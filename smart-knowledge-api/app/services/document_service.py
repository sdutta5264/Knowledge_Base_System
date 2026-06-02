from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from pypdf import PdfReader
import io

from app.models.user import User
from app.models.document import Document
from app.models.chunk import DocumentChunk
from app.schema.document import DocumentResponse, SearchResultItem, ChatRequest, ChatMessage
from app.services.ai_service import AIService

class DocumentService:

    @staticmethod
    async def extract_text(file: UploadFile) -> str:
        file_bytes = await file.read()
        extracted_text = ""

        if file.filename.endswith(".txt"):
            extracted_text = file_bytes.decode("utf-8")

        elif file.filename.endswith(".pdf"):
            pdf_file = io.BytesIO(file_bytes)
            reader = PdfReader(pdf_file)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"
        else:
            raise HTTPException(
                status_code=400,
                detail= "Only .txt and .pdf files are supported."
            )
        if not extracted_text.strip():
            raise  HTTPException(status_code= 400, detail= "Could not extract any meaningful text form the document.")
        return extracted_text

    @classmethod
    async def process_and_save_document(cls, db: Session, file: UploadFile, current_user: User) -> DocumentResponse:
        extracted_content = await cls.extract_text(file)

        db_doc = Document(
            filename= file.filename,
            content= extracted_content,
            user_id= current_user.id
        )

        db.add(db_doc)
        db.commit()
        db.refresh(db_doc)

        text_slices = cls.split_text_into_chunks(extracted_content, chunk_size= 1000, chunk_overlap= 200)

        for index, slice_text in enumerate(text_slices):
            vector_cordinates = AIService.generate_embedding(slice_text)


            db_chunk = DocumentChunk(
                document_id = db_doc.id,
                chunk_text = slice_text,
                chunk_index = index,
                embedding = vector_cordinates
            )
            db.add(db_chunk)

        db.commit()


        return DocumentResponse(
            id= db_doc.id,
            filename= db_doc.filename,
            extracted_characters= len(extracted_content),
            total_chunks_created = len(text_slices),
            msg = "File Processed, sliced and stored successfully"
        )

    @staticmethod
    def split_text_into_chunks(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list[str]:
        """
            Slices a giant block of text into smaller paragraphs.
            Includes a small 'overlap' so sentences that cross boundaries aren't completely lost.
        """

        chunks = []
        start = 0
        text_length = len(text)

        while start < text_length:
            end = min(start + chunk_size, text_length)

            chunk = text[start: end]
            chunks.append(chunk)

            start = start + (chunk_size - chunk_overlap)
        return chunks

    @classmethod
    def search_similar_chunks(cls, db: Session, question: str, user_id: int, top_k: int= 3):
        question_vector = AIService.generate_embedding(question)

        results = (
            db.query(
                DocumentChunk.chunk_text,
                Document.filename,
                ((1 -DocumentChunk.embedding.cosine_distance(question_vector) * 100).label("similarity_score"))
            )
            .join(Document, DocumentChunk.document_id == Document.id)
            .order_by(DocumentChunk.embedding.cosine_distance(question_vector))
            .limit(top_k)
            .all()
        )

        return  [ SearchResultItem.model_validate(row._mapping) for row in results]

    @classmethod
    def process_chat_query(cls, db: Session, request: ChatRequest, user_id: int):
        # 1. MEMORY MANAGEMENT (Summarize if array has more than 6 messages / 3 turns)
        if len(request.chat_history) > 6:
            summary_text = AIService.summarize_conversation(request.chat_history)

            request.chat_history = [
                ChatMessage(role= "System", content= f"Summary of previous chat: {summary_text}")
            ]

        # 2. VECTOR SEARCH
        search_results= cls.search_similar_chunks(db, request.question, user_id, request.top_k)
        context_text= [res.chunk_text for res in search_results]
        unique_sources= list(set(res.document_filename for res in search_results))
        compiled_context= "\n\n--\n\n".join(context_text)

        #3. TEXT GENERATION
        system_prompt = f"Answers the user's question based strictly on this context:\n{compiled_context}"
        print(f"System Prompt--->{system_prompt}")
        final_answer= AIService.generate_chat_response(
            system_prompt= system_prompt,
            chat_history= request.chat_history,
            current_question= request.question
        )

        print("Final Answer:::",final_answer)
        if not final_answer:
            final_answer= "I'm sorry, the AI returned an empty response. This is usually caused by safety filters or an unreadable document chunk."

        #4. STATE SYNCHRONIZATION
        updated_history = request.chat_history.copy()
        updated_history.append(ChatMessage(role= "user", content=request.question))
        updated_history.append(ChatMessage(role="assistant", content=final_answer))

        return {
            "answer": final_answer,
            "source_documents": unique_sources,
            "updated_chat_history": updated_history
        }
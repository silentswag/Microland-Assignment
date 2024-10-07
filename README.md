# OCRifyFlow
OCRifyFlow is a FastAPI-based application that combines _Optical Character_ Recognition (OCR) with a _Question Answering_ (QA) model to extract text from images and answer questions based on the extracted content. 
The application uses _pytesseract_ for OCR and a _DistilBERT_ model for natural language processing.


## API Endpoints
### User Registration:
1. Endpoint: /register
2. Method: POST
3. Description: Registers a new user with a username and password.


### User Login:
4. Endpoint: /login
5. Method: POST
6. Description: Logs in the user and returns a JWT token.


### Upload Image for OCR:
7. Endpoint: /upload
8. Method: POST
9. Description: Uploads an image file (.png) and extracts text using OCR.


### Question Answering:
10. Endpoint: /ask
11. Method: POST
12. Description: Accepts a question based on the extracted text and returns the answer using the QA model.

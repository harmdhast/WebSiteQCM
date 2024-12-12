from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.templating import Jinja2Templates
import uvicorn
import csv
import os
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.datastructures import UploadFile

templates = Jinja2Templates(directory="templates")

# Load all csv
questions = []
csv_file_path = "data.csv"
if os.path.exists(csv_file_path) and os.path.getsize(csv_file_path) > 0:
    with open(csv_file_path, "r", encoding="ISO-8859-1") as file:
        reader = csv.DictReader(
            file,
            fieldnames=[
                "id",
                "question",
                "id2",
                "label",
                "isCorrect",
                "id3",
                "label4",
                "isCorrect5",
                "id6",
                "label7",
                "isCorrect8",
                "id9",
                "label10",
                "isCorrect11",
            ],
            delimiter=";",
        )
        next(reader)  # Skip the header row
        for row in reader:
            question_dict = {
                "id": int(row["id"]),
                "question": row["question"],
                "answers": [
                    {
                        "id": int(row["id2"]),
                        "label": row["label"],
                        "isCorrect": row["isCorrect"].lower() == "true",
                    },
                    {
                        "id": int(row["id3"]),
                        "label": row["label4"],
                        "isCorrect": row["isCorrect5"].lower() == "true",
                    },
                    {
                        "id": int(row["id6"]),
                        "label": row["label7"],
                        "isCorrect": row["isCorrect8"].lower() == "true",
                    },
                    {
                        "id": int(row["id9"]),
                        "label": row["label10"],
                        "isCorrect": row["isCorrect11"].lower() == "true",
                    },
                ],
            }
            questions.append(question_dict)


async def homepage(request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "questions": questions}
    )


async def get_theme(request):
    question_id = int(request.path_params["question_id"])
    question = next((q for q in questions if q["id"] == question_id), None)
    if question:
        return JSONResponse(question)
    return JSONResponse({"error": "Question not found"}, status_code=404)


async def upload_csv(request: Request):
    if request.method == "POST":
        form = await request.form()
        csv_file: UploadFile = form["file"]
        content = await csv_file.read()
        content = content.decode("ISO-8859-1").splitlines()
        reader = csv.DictReader(
            content,
            fieldnames=[
                "id",
                "question",
                "id2",
                "label",
                "isCorrect",
                "id3",
                "label4",
                "isCorrect5",
                "id6",
                "label7",
                "isCorrect8",
                "id9",
                "label10",
                "isCorrect11",
            ],
            delimiter=";",
        )
        next(reader)  # Skip the header row
        global questions
        questions = []
        for row in reader:
            question_dict = {
                "id": int(row["id"]),
                "question": row["question"],
                "answers": [
                    {
                        "id": int(row["id2"]),
                        "label": row["label"],
                        "isCorrect": row["isCorrect"].lower() == "true",
                    },
                    {
                        "id": int(row["id3"]),
                        "label": row["label4"],
                        "isCorrect": row["isCorrect5"].lower() == "true",
                    },
                    {
                        "id": int(row["id6"]),
                        "label": row["label7"],
                        "isCorrect": row["isCorrect8"].lower() == "true",
                    },
                    {
                        "id": int(row["id9"]),
                        "label": row["label10"],
                        "isCorrect": row["isCorrect11"].lower() == "true",
                    },
                ],
            }
            questions.append(question_dict)
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse("upload.html", {"request": request})


routes = [
    Route("/", endpoint=homepage),
    Route("/upload", endpoint=upload_csv, methods=["GET", "POST"]),
]

app = Starlette(debug=True, routes=routes)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

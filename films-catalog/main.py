from fastapi import FastAPI, Request, status, HTTPException

from schemas.movie_catalog import MovieCatalog

app = FastAPI(
    title="Films",
    description="Films catalog",
    version="1.0",
)


@app.get("/")
def root(
    request: Request,
):
    docs_url = request.url.replace(path="/docs")
    return {
        "message": "Hello World",
        "docs_url": str(docs_url),
    }


FILMS_LIST = [
    MovieCatalog(
        id=1,
        title="Удивительное путешествие доктора Дулиттла",
        description="Семь лет назад доктор Дулиттл, прославленный врач-ветеринар, живущий в викторианской Англии, потерял свою жену. Теперь он ведет затворнический образ жизни, скрывшись за высокими стенами своего поместья. Экзотические животные из его коллекции – его единственная компания.",
        year_released=2020,
        rating=6.4,
    ),
    MovieCatalog(
        id=2,
        title="Сделано в Америке",
        description="Он был самым юным пилотом Боинга 747 в США, а уже через несколько лет стал одним из богатейших людей в Америке. Его стиль жизни был столь же экстремальным, как и его бизнес. Закрытые приемы, роскошные блондинки, крутые тачки и рисковые сделки. Он обладал талантом делать деньги из воздуха.",
        year_released=2017,
        rating=7.3,
    ),
    MovieCatalog(
        id=3,
        title="Линкольн",
        description="1865 год. Шестнадцатый президент США Авраам Линкольн находится на пике популярности. Но перед ним стоят серьёзные задачи: провести запрещающую рабство поправку к Конституции через Палату представителей и завершить Гражданскую войну.",
        year_released=2012,
        rating=6.9,
    ),
]


@app.get(
    "/movies",
    response_model=list[MovieCatalog],
)
def get_films_list():
    return FILMS_LIST


@app.get("/movie/{movie_id}", response_model=MovieCatalog)
def get_film(movie_id: int):
    films: MovieCatalog | None = next(
        (film for film in FILMS_LIST if film.id == movie_id),
        None,
    )
    if films:
        return films

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Films not found")

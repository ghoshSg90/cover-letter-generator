from app.services.llm_service import generate_cover_letter

print(
    generate_cover_letter(
        "Microsoft",
        "Senior C++ Engineer",
        "Develop scalable backend systems..."
    )
)

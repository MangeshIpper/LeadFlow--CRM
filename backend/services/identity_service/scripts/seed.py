
from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.organization import Organization


def seed_organization() -> None:
    with SessionLocal() as db:
        existing = db.scalar(
            select(Organization).where(
                Organization.slug == "demo-consulting"
            )
        )

        if existing is not None:
            print("Organization already exists")
            print(f"ID: {existing.id}")
            return

        organization = Organization(
            name="Demo Consulting",
            slug="demo-consulting",
        )

        db.add(organization)
        db.commit()
        db.refresh(organization)

        print("Organization created successfully")
        print(f"ID: {organization.id}")
        print(f"Name: {organization.name}")


if __name__ == "__main__":
    seed_organization()

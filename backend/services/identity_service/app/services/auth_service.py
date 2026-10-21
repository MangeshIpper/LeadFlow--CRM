
from fastapi import HTTPException, status
from psycopg.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User
from app.models.organization import Organization
from app.models.membership import Membership
from app.schemas.auth import RegisterRequest, RegisterResponse


def register_account(
    db: Session,
    payload: RegisterRequest,
) -> RegisterResponse:

    # 1. Hash the password before storing it.
    hashed_password = hash_password(
        payload.password.get_secret_value()
    )

    # 2. Construct the user.
    user = User(
        full_name=payload.full_name,
        email=str(payload.email),
        password_hash=hashed_password,
        is_active=True,
    )

    # 3. Construct the organization.
    organization = Organization(
        name=payload.organization_name,
        slug=payload.organization_slug,
    )

    try:
        # 4. Add both records to the session.
        db.add_all([user, organization])

        # 5. Execute pending inserts to obtain UUIDs.
        db.flush()

        # 6. Associate the user with the organization.
        membership = Membership(
            user_id=user.id,
            organization_id=organization.id,
            role="owner",
        )

        db.add(membership)

        # 7. Persist all three records atomically.
        db.commit()

    except IntegrityError as exc:
        db.rollback()

        # PostgreSQL uniqueness constraint violation.
        if isinstance(exc.orig, UniqueViolation):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "Email or organization slug already exists"
                ),
            ) from exc

        raise

    except Exception:
        db.rollback()
        raise

    # 8. Return only safe, public information.
    return RegisterResponse(
        user_id=user.id,
        organization_id=organization.id,
        email=user.email,
        full_name=user.full_name,
        role="owner",
    )

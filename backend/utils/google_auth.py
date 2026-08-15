"""Verify Google Sign-In ID tokens server-side.

The browser holds a Google ID token (a signed JWT). Decoding it client-side
proves nothing — anyone can mint a base64 blob with any `sub` they like. This
module checks the signature against Google's published keys, so the user ID we
act on is one Google actually issued.

Requires GOOGLE_CLIENT_ID in the environment (the same OAuth client ID the
frontend uses as VITE_GOOGLE_CLIENT_ID) — it is checked as the token audience,
which is what stops a token minted for a *different* site being replayed here.
"""

import logging
import os

from dotenv import load_dotenv
from fastapi import Header, HTTPException
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

load_dotenv()

logger = logging.getLogger("nur-api")

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
# Set AUTH_ENFORCED=false only for local development against a backend with no
# client ID configured. Never set it in production.
AUTH_ENFORCED = os.getenv("AUTH_ENFORCED", "true").lower() not in ("false", "0", "no")

_request = google_requests.Request()  # reuses one session, caches Google's certs


def verify_google_token(token: str) -> dict:
    """Return the token's verified claims, or raise HTTPException(401)."""
    if not GOOGLE_CLIENT_ID:
        raise HTTPException(
            status_code=500,
            detail="GOOGLE_CLIENT_ID is not configured on the server.",
        )
    try:
        claims = id_token.verify_oauth2_token(token, _request, GOOGLE_CLIENT_ID)
    except ValueError as exc:
        # Covers a bad signature, wrong audience, expired token, bad issuer.
        logger.warning("Rejected Google token: %s", exc)
        raise HTTPException(status_code=401, detail="Invalid or expired sign-in.") from exc

    if claims.get("iss") not in ("accounts.google.com", "https://accounts.google.com"):
        raise HTTPException(status_code=401, detail="Invalid token issuer.")
    if not claims.get("sub"):
        raise HTTPException(status_code=401, detail="Token has no subject.")
    return claims


def require_user(user_id: str, authorization: str = Header(default="")) -> str:
    """FastAPI dependency: the caller must prove they are `user_id`.

    Use on every /api/users/{user_id}/... route. Returns the verified user id.
    """
    if not AUTH_ENFORCED:
        logger.warning("AUTH_ENFORCED is off — serving %s unauthenticated.", user_id)
        return user_id

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(status_code=401, detail="Sign-in required.")

    claims = verify_google_token(token)
    if claims["sub"] != user_id:
        # Authenticated, but as somebody else.
        logger.warning("User %s attempted to access %s", claims["sub"], user_id)
        raise HTTPException(status_code=403, detail="You cannot access another user's data.")
    return user_id

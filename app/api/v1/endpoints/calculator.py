from fastapi import APIRouter, HTTPException, Query

from app.services.calculator_service import add, divide, multiply, subtract

router = APIRouter()


@router.get("/calculate")
def calculate(
    left: float = Query(..., description="First number"),
    right: float = Query(..., description="Second number"),
) -> dict[str, object]:
    try:
        return {
            "success": True,
            "data": {
                "left": left,
                "right": right,
                "add": add(left, right),
                "subtract": subtract(left, right),
                "multiply": multiply(left, right),
                "divide": divide(left, right),
            },
            "message": None,
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

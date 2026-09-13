"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND
Mã nguồn chứa danh sách Tool Schemas (JSON Schema) và Execution Layer phục vụ cho MCP Server.
"""

import json
from typing import Dict, Any

# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA (TASK 1.2)
# ==============================================================================

TOOLS_SCHEMA = [
    {
        "name": "route_query",
        "description": "Tra cứu lộ trình, lịch chạy và giá vé tháng của tuyến xe bus điện VinBus theo mã tuyến.",
        "parameters": {
            "type": "object",
            "properties": {
                "route_code": {
                    "type": "string",
                    "description": "Mã tuyến xe cần tra cứu (Ví dụ: 'OCT1')"
                }
            },
            "required": ["route_code"] 
        }
    },
    {
        "name": "register_monthly_ticket",
        "description": "Đăng ký vé tháng VinBus cho khách hàng trên một tuyến xe cụ thể.",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "Mã khách hàng (Ví dụ: KH202602938)"
                },
                "route_code": {
                    "type": "string",
                    "description": "Mã tuyến xe muốn đăng ký vé tháng (Ví dụ: 'E10')"
                },
                "start_date": {
                    "type": "string",
                    "description": "Ngày bắt đầu hiệu lực vé tháng (Ví dụ '13/09/2026')"
                }
            },
            "required": ["customer_id", "route_code", "start_date"] 
        }
    }
]

# ==============================================================================
# 2. MÔ PHỎNG DỮ LIỆU & HÀM THỰC THI TOOL (EXECUTION LAYER)
# ==============================================================================

MOCK_DATABASE = {
    "OCT1": {
        "route_name": "Tuyến OCT1: KĐT Royal City -> Ocean City",
        "stops": ["Times City", "Tòa S2.09", "Tòa S2.15", "Trường Vinschool Ocean Park 2", "Bệnh viện Vinmec"],
        "first_trip": "5:00",
        "last_trip": "23:59",
        "monthly_fare_vnd": 300000,
        "status": "Đang hoạt động"
    },
    "E10": {
        "route_name": "Tuyến E10: KĐT Ocean Park -> Nội Bài",
        "stops": ["Đại học VinUni", "Aeon Mall Long Biên", "Hồ Lâm Du", "Nhà ga hàng hóa Nội Bài", "Sân bay Nội Bài (Nhà ga T2)"],
        "first_trip": "5:00",
        "last_trip": "22:30",
        "monthly_fare_vnd": 250000,
        "status": "Đang hoạt động"
    },
}


def execute_route_query(route_code: str) -> str:
    """Thực thi tra cứu lộ trình tuyến xe theo mã tuyến"""
    route = MOCK_DATABASE.get(route_code.strip().upper())
    if route:
        return json.dumps({
            "status": "SUCCESS",
            "route_code": route_code,
            "data": route
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy tuyến xe có mã '{route_code}'"
        }, ensure_ascii=False)


def execute_register_monthly_ticket(customer_id: str, route_code: str, start_date: str) -> str:
    """Thực thi đăng ký vé tháng VinBus"""
    if route_code.strip().upper() not in MOCK_DATABASE:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tồn tại tuyến {route_code} để đăng ký vé tháng."
        }, ensure_ascii=False)
    return json.dumps({
        "status": "SUCCESS",
        "booking_id": f"TK-{customer_id}-{route_code.upper()}",
        "customer_id": customer_id,
        "route_code": route_code.upper(),
        "start_date": start_date,
        "message": f"Đăng ký vé tháng thành công cho khách hàng {customer_id} trên tuyến {route_code.upper()} từ ngày {start_date}."
    }, ensure_ascii=False)


# Router gọi tool thực tế
TOOL_ROUTER = {
    "route_query": execute_route_query,
    "register_monthly_ticket": execute_register_monthly_ticket
}

def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Hàm trung chuyển thực thi tool"""
    if tool_name in TOOL_ROUTER:
        try:
            return TOOL_ROUTER[tool_name](**arguments)
        except Exception as e:
            return json.dumps({"status": "EXECUTION_ERROR", "error": str(e)}, ensure_ascii=False)
    return json.dumps({"status": "UNKNOWN_TOOL", "error": f"Tool '{tool_name}' không tồn tại!"}, ensure_ascii=False)

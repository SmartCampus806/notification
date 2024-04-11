from datetime import datetime

def make_message(booking_data:dict):
    __normalize_data(booking=booking_data)
    __get_title_from_action(booking=booking_data)

    booking = booking_data.get("booking", {})
    action_text = booking_data.get("action_text", "Данные по бронированию изменились")
    room = booking.get("room", {}).get("value", "")
    owner = booking.get("owner", {}).get("value", "")
    date = booking.get("date")
    start_time = booking.get("startTime", "")
    end_time = booking.get("endTime", "")
    title = booking.get("title", "")
    description = booking.get("description", "")
    status = booking.get("status", "")
    
    tags = ", ".join(tag.get("fullName", "") for tag in booking.get("tags", []))
    groups = ", ".join(group.get("name", "") for group in booking.get("groups", []))
    staff = ", ".join(f"{staff['fullName']}" for staff in booking.get("staff", []))
    
    message =   f"📅 {action_text}: {title} 📅\n\n" \
                f"Аудитория: {room}\n" \
                f"Владелец мероприятия: {owner}\n" \
                f"Дата: {date}\n" \
                f"Время: {start_time} -> {end_time}\n" \
                f"Описание: {description}\n" \
                f"Теги: {tags}\n" \
                f"Группы: {groups if groups != '' else 'Учебных групп нет'}\n" \
                f"Учасники: {staff if staff != '' else 'Других учасников нет'}\n" \
                f"Текущий статус: {status}\n"
              
    return message


months = ["Января", "Февраля", "Марта", "Апреля", "Мая", "Июня", "Июля", "Августа", "Сентября", "Октября", "Ноября", "Декабря"]
def __normalize_data(booking: dict):
    start_time_obj = datetime.fromisoformat(booking.get("booking").get("startTime").replace('Z', '+00:00'))
    end_time_obj = datetime.fromisoformat(booking.get("booking").get("endTime").replace('Z', '+00:00'))

    date = start_time_obj.date()

    booking["booking"]["startTime"] = start_time_obj.time().strftime('%H:%M')
    booking["booking"]["endTime"]   = end_time_obj.time().strftime('%H:%M')
    booking["booking"]["date"]      = f"{date.day} {months[date.month]} {date.year}"
    

def __get_title_from_action(booking: dict):
    if (booking.get("action") == "CREATE"):
        booking["action_text"] = "Новое мероприятияе"

    if (booking.get("action") == "UPDATE"):
        booking["action_text"] = "Мерприятие было изменено"

    if (booking.get("action") == "DELETE"):
        booking["action_text"] = "Мероприятие было отменено"
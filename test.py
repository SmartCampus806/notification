from datetime import datetime

booking = {
	"action": "CREATE",
	"booking": {
		"id": 2,
		"room": {
			"id": 1,
			"value": "Room1"
		},
		"owner": {
			"id": 2,
			"value": "aaaaAAAAAA"
		},
		"startTime": "2023-11-04T09:30:00.000Z",
		"endTime": "2023-11-04T10:50:00.000Z",
		"title": "Лекция по Мат. Анализу",
		"description": "Большое описание",
		"tags": [
			{
				"id": 1,
				"fullName": "Лекция",
				"shortName": "ЛК",
				"color": "#FFFFFF"
			},
			{
				"id": 2,
				"fullName": "Дополнительное",
				"shortName": "ДП",
				"color": "#FFFFFF"
			}
		],
		"groups": [
			{
				"id": 1,
				"name": "M80-410Б-20"
			},
			{
				"id": 2,
				"name": "М80-110М-19"
			}
		],
		"staff": [
			{
				"id": 2,
				"fullName": "aaaaAAAAAA",
				"phoneNumber": "+79297040000",
				"role": "ADMINISTRATOR",
				"isAccountLocked": False
			},
			{
				"id": 3,
				"fullName": "Иванов Иван Иванович",
				"phoneNumber": "+79297040001",
				"role": "ADMINISTRATOR",
				"isAccountLocked": False
			}
		],
		"status": "CONFIRMED"
	}
}



def make_message(booking_data:dict):
    normalize_data(booking=booking_data)
    get_title_from_action(booking=booking_data)

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
    
    message =   f"📅 **{action_text}** 📅\n\n" \
                f"Аудитория: {room}\n" \
                f"Владелец мероприятия: {owner}\n" \
                f"Дата: {date}\n" \
                f"Дата: {date}\n" \
                f"Врем начала: {start_time}\n" \
                f"Врем окончания: {end_time}\n" \
                f"Заголовок: {title}\n" \
                f"Описание: {description}\n" \
                f"Теги: {tags}\n" \
                f"Группы: {groups}\n" \
                f"Учасники: {staff}\n" \
                f"Текущий статус: {status}\n"
              
    return message

months = ["Января", "Февраля", "Марта", "Апреля", "Мая", "Июня", "Июля", "Августа", "Сентября", "Октября", "Ноября", "Декабря"]
def normalize_data(booking: dict):
    start_time_obj = datetime.fromisoformat(booking.get("booking").get("startTime").replace('Z', '+00:00'))
    end_time_obj = datetime.fromisoformat(booking.get("booking").get("endTime").replace('Z', '+00:00'))

    date = start_time_obj.date()

    booking["booking"]["startTime"] = start_time_obj.time().strftime('%H:%M')
    booking["booking"]["endTime"]   = end_time_obj.time().strftime('%H:%M')
    booking["booking"]["date"]      = f"{date.day} {months[date.month]} {date.year}"
    

def get_title_from_action(booking: dict):
    if (booking.get("action") == "CREATE"):
        booking["action_text"] = "Новое мероприятияе"

    if (booking.get("action") == "UPDATE"):
        booking["action_text"] = "Мерприятие было изменено"

    if (booking.get("action") == "DELETE"):
        booking["action_text"] = "Мероприятие было отменено!!!"
        
print(make_message(booking_data=booking))



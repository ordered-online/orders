from django.shortcuts import render


def debug_session(request, session_id):
    return render(request, "orders/debug_session.html", {
        "session_id": session_id
    })



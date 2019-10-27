from django.shortcuts import render


def debug_panel(request, panel_id):
    return render(request, "orders/debug_panel.html", {
        "panel_id": panel_id
    })



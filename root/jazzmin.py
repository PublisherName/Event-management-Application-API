from .env_config import env

JAZZMIN_SETTINGS = {
    "site_title": env.str("SITE_TITLE", "Event Management Admin"),
    "site_header": env.str("SITE_HEADER", "Event Management Admin"),
    "site_brand": env.str("SITE_BRAND", "Event Management"),
    "site_logo": env.path("SITE_LOGO", default="logo/icon.png"),
    "login_logo": None,
    "login_logo_dark": None,
    "site_logo_classes": "img-circle",
    "site_icon": None,
    "welcome_sign": env.str("WELCOME_SIGN", "Welcome to Event Management Admin"),
    "search_model": ["auth.User", "events.Event"],
    "user_avatar": None,
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"app": "events"},
    ],
    "usermenu_links": [
        {"model": "auth.user"},
    ],
    "custom_links": {
        "auth": [
            {
                "name": "Login Tokens",
                "model": "rest_framework.authtoken.TokenProxy",
                "app_label": "auth",
                "url": "/admin/authtoken/tokenproxy/",
                "icon": "fas fa-user-lock",
                "permissions": ["auth.is_superuser", "auth.is_staff"],
            },
            {
                "name": "Activation Tokens",
                "model": "auths.UserActivationToken",
                "app_label": "auths",
                "url": "/admin/auths/useractivationtoken/",
                "icon": "fas fa-user-check",
                "permissions": ["auth.is_superuser", "auth.is_staff"],
            },
            {
                "name": "Reset Tokens",
                "model": "django_rest_passwordreset.ResetPasswordToken",
                "app_label": "auth",
                "url": "/admin/django_rest_passwordreset/resetpasswordtoken/",
                "icon": "fas fa-unlock-alt",
                "permissions": ["auth.is_superuser", "auth.is_staff"],
            },
        ],
    },
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [
        "django_rest_passwordreset.ResetPasswordToken",
        "authtoken.TokenProxy",
        "auths.UserActivationToken",
    ],
    "order_with_respect_to": ["auth", "auths", "events", "preferences", "django_summernote"],
    "icons": {
        # Auth icons
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        # Celery icons
        "django_celery_results": "fas fa-tasks",
        "django_celery_results.taskresult": "fas fa-clipboard-check",
        "django_celery_results.chordcounter": "fas fa-list-ol",
        "django_celery_results.groupresult": "fas fa-layer-group",
        "django_celery_beat": "fas fa-clock",
        "django_celery_beat.periodictask": "fas fa-calendar",
        "django_celery_beat.intervalschedule": "fas fa-hourglass",
        "django_celery_beat.crontabschedule": "fas fa-calendar-alt",
        "django_celery_beat.solarschedule": "fas fa-sun",
        "django_celery_beat.clockedschedule": "fas fa-clock",
        # Django Summernote icons
        "django_summernote": "fas fa-edit",
        "django_summernote.attachment": "fas fa-paperclip",
        # Event icons
        "events": "fas fa-calendar-alt",
        "events.event": "fas fa-calendar",
        "events.eventsignup": "fas fa-tags",
        # Preferences icons
        "preferences": "fas fa-cogs",
        "preferences.emailtemplate": "fas fa-envelope",
        # User Activation Token icons
        "auths": "fas fa-key",
        "auths.useractivationtoken": "fas fa-key",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": False,
    "custom_css": None,
    "custom_js": None,
    "use_google_fonts_cdn": True,
    "show_ui_builder": env.bool("SHOW_UI_BUILDER", False),
    "changeform_format": "horizontal_tabs",
}

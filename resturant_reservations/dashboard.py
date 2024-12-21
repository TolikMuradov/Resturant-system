from grappelli.dashboard import modules, Dashboard

class CustomIndexDashboard(Dashboard):
    """
    Grappelli admin paneli için özelleştirilmiş dashboard.
    """
    def init_with_context(self, context):
        # Uygulamalar listesi
        self.children.append(modules.AppList(
            title="Uygulamalar",
            exclude=('django.contrib.*',),
        ))

        # Hızlı bağlantılar
        self.children.append(modules.LinkList(
            title="Hızlı Erişim",
            children=[
                {'title': 'Ana Site', 'url': '/', 'external': False},
                {'title': 'Admin Paneli', 'url': '/admin', 'external': False},
            ]
        ))

        # İstatistik modülü (isteğe bağlı)
        self.children.append(modules.ModelList(
            title="Model Yönetimi",
            models=['your_app.models.ModelName'],
        ))

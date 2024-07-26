from django.contrib.admin import AdminSite


class RentieAdminSite(AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = "Rentie site admin"

    # Text to put in each page's <h1>.
    site_header = "Rentie administration"

    # Text to put at the top of the admin index page.
    index_title = "Site administration"


rentie_site = RentieAdminSite()

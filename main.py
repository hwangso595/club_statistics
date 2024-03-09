from taipy.gui import Gui, navigate

user = "user"

root_md_admin="<|menu|label=Menu|lov={[('Page-1', 'Page 1'), ('Page-2', 'Page 2')]}|on_action=on_menu|>"
root_md_user="<|menu|label=Menu|lov={[('Page-1', 'Page 1')]}|on_action=on_menu|>"
page1_md="## This is page 1"
page2_md="## This is page 2"


def on_menu(state, action, info):
    page = info["args"][0]
    navigate(state, to=page)


pages_admin = {
    "/": root_md_admin,
    "Page-1": page1_md,
    "Page-2": page2_md
}

pages_user = {
    "/": root_md_user,
    "Page-1": page1_md,
}
if user == "admin":
    Gui(pages=pages_admin).run()
else:
    Gui(pages=pages_user).run()
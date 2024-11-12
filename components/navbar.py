from collections import defaultdict

import dash_mantine_components as dmc
from dash_iconify import DashIconify



def create_main_link(icon, label, href):
    return dmc.Anchor(
        dmc.Group(
            [
                DashIconify(
                    icon=icon,
                    width=23,
                    #color=dmc.DEFAULT_THEME["colors"][PRIMARY_COLOR][5],
                ),
                dmc.Text(label, size="sm"),
            ]
        ),
        href=href,
        variant="text",
        mb=5,
        underline=False,
    )


def create_content(data):


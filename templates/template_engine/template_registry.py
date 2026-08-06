"""
==================================================
ForgePy
Template Registry
==================================================
"""

from templates.basic.basic_template import BasicTemplate


class TemplateRegistry:

    def __init__(self):

        self.templates = {
            "basic": BasicTemplate(),
        }

    def get(
        self,
        name: str,
    ):

        return self.templates[name]

    def list_templates(self):

        return self.templates
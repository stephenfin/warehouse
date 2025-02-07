# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from jinja2 import Environment, FileSystemLoader

import warehouse

FILTERS = {
    "format_date": "warehouse.i18n.filters:format_date",
    "format_datetime": "warehouse.i18n.filters:format_datetime",
    "format_rfc822_datetime": "warehouse.i18n.filters:format_rfc822_datetime",
    "format_number": "warehouse.i18n.filters:format_number",
    "format_classifiers": "warehouse.filters:format_classifiers",
    "classifier_id": "warehouse.filters:classifier_id",
    "format_tags": "warehouse.filters:format_tags",
    "json": "warehouse.filters:tojson",
    "camoify": "warehouse.filters:camoify",
    "shorten_number": "warehouse.filters:shorten_number",
    "urlparse": "warehouse.filters:urlparse",
    "contains_valid_uris": "warehouse.filters:contains_valid_uris",
    "format_package_type": "warehouse.filters:format_package_type",
    "parse_version": "warehouse.filters:parse_version",
    "localize_datetime": "warehouse.filters:localize_datetime",
    "canonicalize_name": "packaging.utils:canonicalize_name",
}


def test_templates_for_empty_titles():
    """
    Test if all HTML templates have defined the title block. See
    https://github.com/pypa/warehouse/issues/784
    """
    dir_name = os.path.join(os.path.dirname(warehouse.__file__), "templates")

    env = Environment(
        loader=FileSystemLoader(dir_name),
        extensions=[
            "jinja2.ext.i18n",
            "warehouse.utils.html.ClientSideIncludeExtension",
        ],
        cache_size=0,
    )

    env.filters.update(FILTERS)

    for dir_, _, files in os.walk(dir_name):
        if (
            dir_.find("/includes") > -1
            or dir_.find("/api") > -1
            or dir_.find("/legacy") > -1
            or dir_.find("/email/") > -1
        ):
            continue

        for file_name in files:
            if file_name.endswith(".csi.html"):
                continue
            if file_name.endswith(".html"):
                rel_dir = os.path.relpath(dir_, dir_name)
                rel_file = os.path.join(rel_dir, file_name)
                template = env.get_template(rel_file)
                assert "title" in template.blocks or "title_base" in template.blocks


def test_render_templates():
    """
    Test if all HTML templates are rendered without Jinja exceptions.
    see https://github.com/pypa/warehouse/issues/6634
    """
    dir_name = os.path.join(os.path.dirname(warehouse.__file__), "templates")

    env = Environment(
        loader=FileSystemLoader(dir_name),
        extensions=[
            "jinja2.ext.i18n",
            "warehouse.utils.html.ClientSideIncludeExtension",
        ],
        cache_size=0,
    )

    env.filters.update(FILTERS)

    exceptions = []
    for dir_, _, files in os.walk(dir_name):
        for file_name in files:
            if file_name.endswith(".html"):
                rel_dir = os.path.relpath(dir_, dir_name)
                rel_file = os.path.join(rel_dir, file_name)
                try:
                    env.get_template(rel_file)
                except Exception as e:
                    exceptions.append(e)

    assert len(exceptions) == 0

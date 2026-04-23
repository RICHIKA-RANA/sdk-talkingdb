from talkingdb_sdk.client import TalkingDBClient

document = {
    "layouts": [
        {
            "orientation": "PORTRAIT",
            "header": {
                "runs": [],
                "type": "Header",
                "id": "doc::55816ee3:layout::0:header::0"
            },
            "footer": {
                "runs": [],
                "type": "Footer",
                "id": "doc::55816ee3:layout::0:footer::0"
            },
            "elements": [
                {
                    "style": {
                        "name": "Heading 3",
                        "space_before": 7.1,
                        "space_after": 5.95,
                        "font_size": 14
                    },
                    "runs": [
                        {
                            "text": "Introduction",
                            "attributes": {
                                "bold": True,
                                "font_size": 14,
                                "styles": [
                                    "Default Paragraph Font",
                                    "font:Liberation Serif"
                                ]
                            },
                            "type": "Run",
                            "id": "doc::55816ee3:layout::0:para::0:run::0"
                        }
                    ],
                    "type": "Paragraph",
                    "id": "doc::55816ee3:layout::0:para::0",
                    "is_caption": False,
                    "is_heading": True,
                    "heading_level": 3,
                    "is_example": False,
                    "is_hidden": False,
                    "is_instruction": False,
                    "is_list": False,
                    "list_level": 0,
                    "is_toc": False,
                    "is_lot": False,
                    "is_lof": False,
                    "is_loa": False,
                    "is_footnote": False
                },
                {
                    "style": {
                        "name": "Normal",
                        "space_before": 12,
                        "space_after": 7.1
                    },
                    "runs": [
                        {
                            "text": "This document provides a brief overview of a sample project. It demonstrates how a single-page document can be structured using clear headings, concise paragraphs, and simple formatting. The goal is to maintain readability while presenting essential information effectively.",
                            "attributes": {
                                "font_size": 12,
                                "styles": [
                                    "Default Paragraph Font",
                                    "font:Aptos"
                                ]
                            },
                            "type": "Run",
                            "id": "doc::55816ee3:layout::0:para::1:run::0"
                        }
                    ],
                    "type": "Paragraph",
                    "id": "doc::55816ee3:layout::0:para::1",
                    "parent_ref_id": "doc::55816ee3:layout::0:para::0",
                    "is_caption": False,
                    "is_heading": False,
                    "is_example": False,
                    "is_hidden": False,
                    "is_instruction": False,
                    "is_list": False,
                    "list_level": 0,
                    "is_toc": False,
                    "is_lot": False,
                    "is_lof": False,
                    "is_loa": False,
                    "is_footnote": False
                },
                {
                    "style": {
                        "name": "Heading 3",
                        "space_before": 7.1,
                        "space_after": 5.95,
                        "font_size": 14
                    },
                    "runs": [
                        {
                            "text": "Objective",
                            "attributes": {
                                "bold": True,
                                "font_size": 14,
                                "styles": [
                                    "Default Paragraph Font",
                                    "font:Liberation Serif"
                                ]
                            },
                            "type": "Run",
                            "id": "doc::55816ee3:layout::0:para::2:run::0"
                        }
                    ],
                    "type": "Paragraph",
                    "id": "doc::55816ee3:layout::0:para::2",
                    "is_caption": False,
                    "is_heading": True,
                    "heading_level": 3,
                    "is_example": False,
                    "is_hidden": False,
                    "is_instruction": False,
                    "is_list": False,
                    "list_level": 0,
                    "is_toc": False,
                    "is_lot": False,
                    "is_lof": False,
                    "is_loa": False,
                    "is_footnote": False
                },
                {
                    "style": {
                        "name": "Normal",
                        "space_before": 12,
                        "space_after": 7.1
                    },
                    "runs": [
                        {
                            "text": "The objective of this project is to build a scalable and efficient system that addresses user needs while maintaining high performance and reliability. The design focuses on simplicity, modularity, and ease of maintenance.",
                            "attributes": {
                                "font_size": 12,
                                "styles": [
                                    "Default Paragraph Font",
                                    "font:Aptos"
                                ]
                            },
                            "type": "Run",
                            "id": "doc::55816ee3:layout::0:para::3:run::0"
                        }
                    ],
                    "type": "Paragraph",
                    "id": "doc::55816ee3:layout::0:para::3",
                    "parent_ref_id": "doc::55816ee3:layout::0:para::2",
                    "is_caption": False,
                    "is_heading": False,
                    "is_example": False,
                    "is_hidden": False,
                    "is_instruction": False,
                    "is_list": False,
                    "list_level": 0,
                    "is_toc": False,
                    "is_lot": False,
                    "is_lof": False,
                    "is_loa": False,
                    "is_footnote": False
                },
                {
                    "style": {
                        "name": "Heading 3",
                        "space_before": 7.1,
                        "space_after": 5.95,
                        "font_size": 14
                    },
                    "runs": [
                        {
                            "text": "Implementation Approach",
                            "attributes": {
                                "bold": True,
                                "font_size": 14,
                                "styles": [
                                    "Default Paragraph Font",
                                    "font:Liberation Serif"
                                ]
                            },
                            "type": "Run",
                            "id": "doc::55816ee3:layout::0:para::4:run::0"
                        }
                    ],
                    "type": "Paragraph",
                    "id": "doc::55816ee3:layout::0:para::4",
                    "is_caption": False,
                    "is_heading": True,
                    "heading_level": 3,
                    "is_example": False,
                    "is_hidden": False,
                    "is_instruction": False,
                    "is_list": False,
                    "list_level": 0,
                    "is_toc": False,
                    "is_lot": False,
                    "is_lof": False,
                    "is_loa": False,
                    "is_footnote": False
                },
                {
                    "style": {
                        "name": "Normal",
                        "space_before": 12,
                        "space_after": 7.1
                    },
                    "runs": [
                        {
                            "text": "The system is implemented using modern development practices. A modular architecture ensures that each component can be developed and tested independently. APIs are designed to be lightweight and performant, enabling seamless integration with other services.",
                            "attributes": {
                                "font_size": 12,
                                "styles": [
                                    "Default Paragraph Font",
                                    "font:Aptos"
                                ]
                            },
                            "type": "Run",
                            "id": "doc::55816ee3:layout::0:para::5:run::0"
                        }
                    ],
                    "type": "Paragraph",
                    "id": "doc::55816ee3:layout::0:para::5",
                    "parent_ref_id": "doc::55816ee3:layout::0:para::4",
                    "is_caption": False,
                    "is_heading": False,
                    "is_example": False,
                    "is_hidden": False,
                    "is_instruction": False,
                    "is_list": False,
                    "list_level": 0,
                    "is_toc": False,
                    "is_lot": False,
                    "is_lof": False,
                    "is_loa": False,
                    "is_footnote": False
                },
                {
                    "style": {
                        "name": "Heading 3",
                        "space_before": 7.1,
                        "space_after": 5.95,
                        "font_size": 14
                    },
                    "runs": [
                        {
                            "text": "Conclusion",
                            "attributes": {
                                "bold": True,
                                "font_size": 14,
                                "styles": [
                                    "Default Paragraph Font",
                                    "font:Liberation Serif"
                                ]
                            },
                            "type": "Run",
                            "id": "doc::55816ee3:layout::0:para::6:run::0"
                        }
                    ],
                    "type": "Paragraph",
                    "id": "doc::55816ee3:layout::0:para::6",
                    "is_caption": False,
                    "is_heading": True,
                    "heading_level": 3,
                    "is_example": False,
                    "is_hidden": False,
                    "is_instruction": False,
                    "is_list": False,
                    "list_level": 0,
                    "is_toc": False,
                    "is_lot": False,
                    "is_lof": False,
                    "is_loa": False,
                    "is_footnote": False
                },
                {
                    "style": {
                        "name": "Normal",
                        "space_before": 12,
                        "space_after": 7.1
                    },
                    "runs": [
                        {
                            "text": "This sample document illustrates how to organize content within a single page. By using structured sections and concise language, it ensures clarity and professionalism. This format is suitable for reports, summaries, and project overviews.",
                            "attributes": {
                                "font_size": 12,
                                "styles": [
                                    "Default Paragraph Font",
                                    "font:Aptos"
                                ]
                            },
                            "type": "Run",
                            "id": "doc::55816ee3:layout::0:para::7:run::0"
                        }
                    ],
                    "type": "Paragraph",
                    "id": "doc::55816ee3:layout::0:para::7",
                    "parent_ref_id": "doc::55816ee3:layout::0:para::6",
                    "is_caption": False,
                    "is_heading": False,
                    "is_example": False,
                    "is_hidden": False,
                    "is_instruction": False,
                    "is_list": False,
                    "list_level": 0,
                    "is_toc": True,
                    "is_lot": False,
                    "is_lof": False,
                    "is_loa": False,
                    "is_footnote": False
                }
            ],
            "type": "Layout",
            "id": "doc::55816ee3:layout::0"
        }
    ],
    "type": "Document",
    "id": "doc::55816ee3",
    "filename": "Document1.docx"
}

metadata = {
    "scope": "org",
    "event_group_id": "",
    "trigger_event_id": "",
    "additionalProp1": {}
}

talkingDB = TalkingDBClient("http://localhost:8090", 300, {"Authorization": "Bearer LdE75NQFk2YFpIAWQvE0IY5Q1L2WUcvKOYOwZNf09_Q"})

index = talkingDB.index_document(document, metadata)

print(index)

matches = talkingDB.match_node([index], "objective", 1, metadata)

print(matches)

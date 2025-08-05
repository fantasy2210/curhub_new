import json, os
from django.core.management import call_command
from django.test import SimpleTestCase
from io import StringIO
from daotao.services import import_program_from_docx

class ImportProgramServiceTests(SimpleTestCase):
    def test_import_service_invokes_langextract(self):
        # stub docx.Document
        class FakeCell:
            def __init__(self, text):
                self.text = text

        class FakeRow:
            def __init__(self):
                self.cells = [FakeCell('val1'), FakeCell('val2')]

        class FakeTable:
            rows = [FakeRow(), FakeRow()]

        import daotao.services.docx as docx_mod
        original_docx = docx_mod.Document
        docx_mod.Document = lambda path: type('Doc', (), {'tables': [FakeTable()]})

        import daotao.services as services_mod
        expected = {"program_code": "P1", "courses": []}
        services_mod.lx.extract = lambda **kwargs: expected

        result = import_program_from_docx('dummy.docx')
        self.assertEqual(result, expected)

        docx_mod.Document = original_docx

class ImportTrainingProgramCommandTests(SimpleTestCase):
    def test_command_outputs_json(self):
        import daotao.services as services_mod
        expected = {"a": 1}
        services_mod.import_program_from_docx = lambda path: expected

        out = StringIO()
        call_command('import_training_program', 'dummy.docx', stdout=out)
        output = out.getvalue()
        self.assertIn('"a": 1', output)
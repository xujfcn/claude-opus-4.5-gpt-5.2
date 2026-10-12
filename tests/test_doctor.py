import importlib.util
import json
from pathlib import Path
import unittest
spec = importlib.util.spec_from_file_location('doctor', Path(__file__).parents[1] / 'tools/doctor.py')
d = importlib.util.module_from_spec(spec); spec.loader.exec_module(d)

class DoctorTests(unittest.TestCase):
    def test_offline_never_calls_network(self):
        def fail(*args): self.fail('network in offline mode')
        self.assertFalse(d.diagnose('chat', 'https://crazyrouter.com/v1', 'gpt-4o-mini', transport=fail)['errors'])
    def test_bad_urls_block_network_and_redact(self):
        for base in ['https://crazyrouter.com/v1/v1', 'https://crazyrouter.com/v1?key=SECRET', 'https://evil.example/v1', 'https://SECRET@crazyrouter.com/v1']:
            result = d.diagnose('chat', base, 'gpt-4o-mini', online=True, transport=lambda *a:self.fail('invalid URL used'))
            self.assertTrue(result['errors']); self.assertNotIn('SECRET', json.dumps(result))
    def test_auth_failure_stops_inference(self):
        calls=[]
        def fake(*a): calls.append(a); return 401, None
        r=d.diagnose('chat','https://crazyrouter.com/v1','gpt-4o-mini','SECRET',inference=True,transport=fake)
        self.assertEqual(len(calls),1); self.assertNotIn('SECRET',json.dumps(r));self.assertTrue(r['errors'])
    def test_alias_absence_does_not_block_explicit_inference(self):
        calls=[]
        def fake(*a):
            calls.append(a)
            return (200,{'data':[]}) if len(calls)==1 else (200,{'choices':[{'message':{'content':'OK'}}]})
        r=d.diagnose('chat','https://crazyrouter.com/v1','alias','secret',inference=True,transport=fake)
        self.assertFalse(r['errors']);self.assertFalse(r['checks'][0]['model_listed']);self.assertTrue(r['checks'][1]['has_output'])
    def test_protocol_shapes(self):
        self.assertIn('input',d.body_for('responses','id'))
        self.assertIn('contents',d.body_for('gemini','id'))
        self.assertIn('max_tokens',d.body_for('messages','id'))
        self.assertFalse(d.has_output('responses',{'output':[{'type':'reasoning'}]}))

if __name__=='__main__':unittest.main()

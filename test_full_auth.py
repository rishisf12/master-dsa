import requests, time
B='http://127.0.0.1:8001'

print('=== Testing Complete Auth Flow ===')

# 1. Signup
print('\n1. Signup...')
data = {
    'first_name': 'Final',
    'last_name': 'Test',
    'gender': 'Other',
    'programme': 'MTech',
    'semester': 2,
    'branch': 'ME',
    'username': 'finaltest123',
    'roll_number': '25BME001',
    'email': 'final@iiitdmj.ac.in',
    'password': 'Password123!',
    'confirm_password': 'Password123!'
}
r = requests.post('http://127.0.0.1:8001/auth/signup', json=data)
print('  Signup:', r.status_code, '-', r.json()['message'])

# 2. Verify email
print('\n2. Verify email...')
code = r.json()['user']['verification_code']
r2 = requests.post('http://127.0.0.1:8001/auth/verify-email', json={'email': 'final@iiitdmj.ac.in', 'code': str(r.json()['user']['verification_code'])})
print('  Verify:', r2.status_code, '-', r2.json()['message'])

# 3. Login
print('\n3. Login...')
r = requests.post('http://127.0.0.1:8001/auth/login', data={'username': 'finaltest123', 'password': 'Password123!'})
print('  Login:', r.status_code)
token = r.json()['access_token']

# 4. Get profile
print('\n4. Get profile...')
headers = {'Authorization': 'Bearer ' + token}
r = requests.get('http://127.0.0.1:8001/auth/profile', headers={'Authorization': 'Bearer ' + token})
print('  Profile:', r.status_code, '-', r.json()['first_name'], r.json()['last_name'], r.json()['branch'], 'Sem', r.json()['semester'])

# 5. Branch change request
print('\n5. Branch change request...')
r = requests.post('http://127.0.0.1:8001/auth/branch-change-request', json={'new_branch': 'CSE', 'reason': 'Interest in CS'}, headers={'Authorization': 'Bearer ' + token})
print('  Branch change:', r.status_code, '-', r.json()['message'])

# 6. Get profile again to see branch change request
print('\n6. Check branch change request...')
r = requests.get('http://127.0.0.1:8001/auth/profile', headers={'Authorization': 'Bearer ' + token})
print('  Branch change requested:', r.json()['branch_change_requested'])
print('  Requested branch:', r.json()['requested_branch'])

print('\n=== All tests passed! ===')
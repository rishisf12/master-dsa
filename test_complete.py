import requests, random, time, sqlite3
B='http://127.0.0.1:8001'

print('=== FULL AUTH FLOW TEST ===')

# 1. Signup
num = random.randint(10000, 99999)
data = {
    'first_name': 'Final',
    'last_name': 'Test',
    'gender': 'Male',
    'programme': 'BTech',
    'semester': 5,
    'branch': 'CSE',
    'username': 'finaltest{}'.format(num),
    'roll_number': '24BCS{:05d}'.format(num),
    'email': 'finaltest{}@iiitdmj.ac.in'.format(num),
    'password': 'Password123!',
    'confirm_password': 'Password123!'
}
r = requests.post(B+'/auth/signup', json=data)
print('1. Signup:', r.status_code)
print('   Verification code in response:', r.json().get('user', {}).get('verification_code', 'N/A'))

# 2. Verify email using code from DB
con = sqlite3.connect('C:/Users/Appex/Documents/Default Project/CampusPilot/database/classpilot.db')
cur = con.cursor()
cur.execute('SELECT email_verification_code FROM user WHERE email = ?', ('finaltest{}@iiitdmj.ac.in'.format(num),))
row = cur.fetchone()
code = row[0] if row else None
print('Code in DB:', code)

if code:
    r2 = requests.post(B+'/auth/verify-email', json={'email': 'finaltest{}@iiitdmj.ac.in'.format(num), 'code': str(code)})
    print('Verify:', r2.status_code, r2.json())

# 3. Login
r = requests.post(B+'/auth/login', data={'username': 'finaltest{}'.format(num), 'password': 'Password123!'})
print('Login:', r.status_code)
if r.status_code == 200:
    token = r.json()['access_token']
    headers = {'Authorization': 'Bearer ' + token}
    
    # Get profile
    r = requests.get(B+'/auth/profile', headers={'Authorization': 'Bearer ' + token})
    print('Profile:', r.status_code, r.json())
    
    # Branch change request
    r = requests.post(B+'/auth/branch-change-request', json={'new_branch': 'ECE', 'reason': 'Interest in ECE'}, headers=headers)
    print('Branch change:', r.status_code, r.json())
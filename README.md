# IAM-User-PrivEsc

### An IAM user with 0 policies attached to it / nor added to any group still can assume roles!
┌─────────────────────────────────────────────────────────────┐
│ Step 1: Compromised/Created Unprivileged IAM User           │
│ • User: "hacker"                                            │
│ • Attached Policies: NONE                                   │
│ • Group Memberships: NONE                                   │
│ • Expected Permissions: NONE                                │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 2: Discover/Create Role with Wildcard Trust            │
│ • Role: "compromised-cie-engineer"                          │
│ • Trust Policy: {"AWS": "*"}                                │
│ • Attached Policy: AdministratorAccess                      │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 3: Privilege Escalation                                │
│ • Unprivileged user calls sts:AssumeRole                    │
│ • Trust policy allows it (despite no user permissions!)     │
│ • Returns temporary admin credentials                       │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 4: Unrestricted Lateral Movement                       │
│ • Full administrator access achieved                        │
│ • Can access all AWS services                               │
│ • Can create backdoors, exfiltrate data, destroy resources  │
└─────────────────────────────────────────────────────────────┘

<img width="3360" height="1280" alt="image" src="https://github.com/user-attachments/assets/dfa05f5c-e94d-4114-aba4-c25edfd13bae" />

<img width="2780" height="1170" alt="image" src="https://github.com/user-attachments/assets/2c37e03c-3ef8-4e04-9bbe-76c9a7680930" />

<img width="3354" height="1440" alt="image" src="https://github.com/user-attachments/assets/a00486cb-fadc-48e7-8c6a-d2f0e8d91181" />

<img width="3584" height="2262" alt="image" src="https://github.com/user-attachments/assets/6e0366bc-9874-4040-9c71-6f4936c9c404" />


### Automated Demo :

<img width="3584" height="2262" alt="image" src="https://github.com/user-attachments/assets/bcd3dcd5-ac50-4522-97e3-eaed10f11972" />



# V16 – setup (10 minutes, 3 secrets)

V16 runs in this **public** repository. Your CV and your application packs never enter it:
the CV is a secret, and every pack is **emailed to you**. The public page shows only the job list.

## 1. Files
Main folder: `agent.py`, `save.py`, `SETUP.md`. Workflow: `.github/workflows/v16.yml`.
`README.md` and `jobs.json` are written by the agent – don't edit them.

## 2. Gmail app password
1. Turn on **2-Step Verification** for your Google account.
2. Go to **myaccount.google.com/apppasswords** → name it `V16` → **Create** → copy the 16 characters.

## 3. Secrets – V16 → Settings → Secrets and variables → Actions → **Secrets** tab → New repository secret
| Name | Value |
|---|---|
| `MASTER_CV` | Your full CV as plain text (under 7,000 characters) |
| `MAIL_USER` | Your Gmail address |
| `MAIL_PASS` | The 16-character app password |
| `MAIL_TO` *(optional)* | Another address to receive the packs |
| `SEARCH_API_KEY` *(optional)* | Brave Search API key, for salary evidence from the web |

Use **Repository secrets** (not Environment or Dependabot). Names exactly as written.

## 4. One setting
**Settings → Actions → General → Workflow permissions → Read and write permissions → Save.**

## 5. First run
**Actions → V16 → Run workflow → Run workflow.** A green ✓ and the job table on the Code tab mean it works.
A branch `agent-lock` appears – don't delete it (it holds the AI budget counter, hashed only).

## Using it
- **Automatic:** searches every 5 minutes; emails up to `PACKS_PER_DAY` packs a day (High/Medium fit, most urgent first).
- **One job now:** Actions → V16 → Run workflow → paste the job's link (+ language, focus) → Run workflow.
- **Login-only sites (LinkedIn, Workday…), privately from your phone:** send an email **from your Gmail to yourself**
  with a subject starting **`JOB`** (e.g. `JOB: Site Engineer STRABAG`). Put the job link and the **full job text** in the body.
  Picked up within ~5 minutes; the email is marked as read when done. Emails from anyone else are ignored.
- **Each pack email:** analysis + HR prescreening + ATS + salary + check-list, with `CV.docx`, `Cover_Letter.docx` and the full report.
- **Emergency stop:** Settings → Secrets and variables → Actions → **Variables** tab → New variable `AI_ENABLED` = `no`.

## Warnings on the front page
| Warning | Fix |
|---|---|
| Setup not finished – add these secrets: … | Add the listed secrets (step 3) |
| Email not usable: Gmail refused the app password | New app password → update `MAIL_PASS` (changing your Google password revokes it) |
| Update needed in v16.yml: actions/checkout@vX → @vY | Edit the workflow file, change the number; the warning clears on the next run |
| AI is switched off | Delete the `AI_ENABLED` variable |
| Red ✗ on "Save" | Step 4 (Read and write permissions) |

Changing the **first two lines of your CV** (name and contact line) or your Gmail address resets the agent's memory of which
jobs already got a pack, so some packs may be made once more (still within the daily limits).

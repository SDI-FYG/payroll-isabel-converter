# FLYINGGROUP · Payroll → Isabel SEPA converter

Internal tool for the FLYINGGROUP accounting team. It converts payroll instruction files (PDF or Excel) from the payroll administrator into a SEPA credit transfer file (pain.001.001.09) for upload in Isabel 6.

## Access

The site is protected by a login. `index.html` holds the application **encrypted** (AES-256-GCM, with the key derived via PBKDF2-SHA256 and 600,000 iterations). The page is only decrypted in the browser after a valid account and password are entered. The credentials are not stored in this repository. Ask Finance for access.

- The login lasts as long as the browser tab is open. Click **Log out** in the header to close it earlier.
- Use Microsoft Edge or Google Chrome.

## Data protection

- Payroll files and the masterdata Excel are read **locally in the browser**. Nothing is uploaded or sent to a server.
- The masterdata file (`Masterdata_Payroll_Beneficiaries.xlsx`) stays on OneDrive and must **never** be committed. `.gitignore` blocks `xlsx`, `pdf`, `xml` and `csv` files.

## Publish on GitHub Pages

1. Create a repository, for example `payroll-isabel-converter`. A private repository is recommended; GitHub Pages for private repositories needs a GitHub Team or Enterprise plan.
2. Upload `index.html`, `.nojekyll`, `.gitignore`, `README.md`, `THIRD_PARTY_NOTICES.md` and the `tools/` folder.
3. Go to **Settings → Pages → Build and deployment**, choose *Deploy from a branch*, then branch `main` and folder `/ (root)`. Save.
4. After a minute the tool is available at `https://<organisation>.github.io/payroll-isabel-converter/`.

## Update the application or change the password

The unencrypted converter (`Payroll_Isabel_Converter.html`) is kept in the OneDrive folder `ISABEL\MASTERDATA`, not in this repository.

```bash
pip install cryptography
python tools/build_protected.py "<path>/Payroll_Isabel_Converter.html" -o index.html
# the script asks for the account and the (new) password
```

Commit the new `index.html`. Changing the password means rebuilding `index.html`: users who are logged in keep access only until they close their tab.

## Note on security

This is client-side protection on a static site. Without the correct account and password the code cannot be read. With them, anyone can open the tool, so share the password only with the accounting team, choose a strong one, and rebuild with a new password when people leave. Payroll data itself is never stored on the site.

<p align="center"><b>English</b> · <a href="SECURITY.ar.md">العربية</a></p>

# Security in WordPress SEO Blog Publisher

## Who is the publisher?

[Marsad Labs](https://labs.marsadgroup.co) is the product arm of Marsad Group, a UK-registered marketing agency. [About us](https://labs.marsadgroup.co/about-us/) · [Privacy policy](https://labs.marsadgroup.co/privacy-policy/)

## What does this skill do with your data?

| Question | Answer |
|---|---|
| **Login details** | They stay in a `sites.txt` file on your computer. They are never uploaded with the skill or printed. |
| **What does it connect to?** | The `wp.py` script connects only to the WordPress sites you list in that file. |
| **Does it publish on its own?** | Yes, when you ask it to publish a post: it creates a Draft first and then publishes it. Use an Application Password with suitable permissions. |
| **Code** | One script built on the Python standard library, open for you to read. |

## Scan result

- **Tool:** SkillSpector, an automated scan that does not send the files to any external model.
- **Automated risk score:** 40/100, rated medium.
- **Alerts:** 0 critical, 1 high, 4 medium, 0 low.
- **Main cause of the alerts after manual review:** The alert comes from a sentence about RankMath warnings in the instructions, not from code.
- **Review limits:** we reviewed the critical and high alerts by hand. Scanning reduces risk but is not a full guarantee, so check the permissions before using any skill.

## Verify the file

Every release on the Releases page includes a `SHA256SUMS.txt` file. Compare the hash of your download with the one listed there:

```powershell
Get-FileHash .\wordpress-seo-blog-publisher.zip -Algorithm SHA256
```

## Found a security problem?

Send it to `Labs@marsadgroup.co` and please do not disclose it publicly until it is fixed.

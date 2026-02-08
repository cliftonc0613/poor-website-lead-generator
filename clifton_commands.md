# Command System for Clifton

🎯 **Just tell me what you want to analyze and I'll run it for you!**

## 🚀 How It Works

**You give me commands like:**
- "analyze https://business1.com https://business2.net"  
- "check oldschoolhvac.com"
- "find hvac greenville"
- "search plumber spartanburg"

**I automatically:**
1. Run the Python analysis
2. Show you formatted results  
3. Highlight hot leads (score < 30)
4. Save detailed CSV file
5. Extract contact info when found

## 📋 Command Examples

### 🌐 Analyze Websites
```
"analyze https://hvaccompany.com https://plumbingservice.net"
"check business-website.org" 
"test https://landscaping.com http://contractor.net"
```

### 🔍 Get Search Patterns  
```
"find hvac greenville"
"search plumber spartanburg"
"look for landscaping anderson"
"get contractors upstate sc"
```

## 📊 What You'll Get Back

### 🔥 Hot Leads (Score < 30)
```
🔥 HOT LEAD: ABC HVAC (Score: 22)
   🌐 https://abchvac.com
   📞 (864) 555-0123
   ⚠️ Issues: No HTTPS, No mobile viewport, Outdated copyright: 2018
```

### 💡 Good Prospects (Score 30-49)
```
💡 GOOD PROSPECT: Quick Plumbing (Score: 35)
   🌐 http://quickplumbing.net
   📧 info@quickplumbing.net
   ⚠️ Issues: No HTTPS, Contains Lorem ipsum
```

### ✅ Unlikely (Score 50+)
```
✅ UNLIKELY: Modern Landscaping (Score: 85)
   🌐 https://modernlandscaping.com
   📞 (864) 555-0456
   📧 contact@modernlandscaping.com
```

## ⚡ Quick Command Reference

| What You Say | What I Do |
|--------------|-----------|
| "analyze [URLs]" | Run full website analysis |
| "check [URL]" | Analyze single website |
| "find hvac greenville" | Show Google search patterns |
| "search [service] [location]" | Get targeted search queries |

## 📈 Automatic Features

✅ **Quality scoring** (0-100, lower = better prospect)  
✅ **Hot lead detection** (critical issues flagged)  
✅ **Contact extraction** (phone/email when found)  
✅ **CSV export** with full data  
✅ **Issue identification** (HTTPS, mobile, copyright, etc.)  

## 💡 Workflow

**You:** "find hvac greenville"  
**Me:** [Shows Google search patterns]  

**You:** [Copy searches, find URLs, then say] "analyze https://business1.com https://business2.com"  
**Me:** [Runs analysis, shows hot leads and prospects]  

**You:** Open the CSV file to see full details and contact info

---

**🎯 Ready! Just give me a command and I'll handle the rest.**
# 📄 Resumate - Because Your Resume Deserves Better Than MS Word

[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Resume Power Level](https://img.shields.io/badge/Resume%20Power%20Level-Over%209000!-red.svg)]()

> *"I spent 25 years mastering technology, then realized my resume still looked like it was made in 1995. So I fixed that."* - Chris, probably

## 🚀 What The Hell Is This?

Resumate is a Python-powered resume generator that treats your career like the engineering project it deserves to be. No more fighting with Word margins at 2 AM. No more "why did my bullet points just explode?" Just clean YAML in, gorgeous PDF out.

Built by someone who:
- ✅ Automated 20,000+ VMs
- ✅ Managed enterprise infrastructure  
- ❌ Refused to manually format another resume ever again

## ✨ Features That Actually Matter

- **YAML-Powered**: Your resume data in clean, version-controllable YAML
- **Template Engine**: Multiple templates from classic to "wow, how'd you do that?"
- **Skill Ratings**: Visual skill bars because lists are boring
- **Icon Support**: 1000+ tech icons from DevIcons, Font Awesome, Simple Icons
- **QR Codes**: For when you want to be *that* person (in a good way)
- **Two-Page Support**: Different layouts for page 1 and continuation pages
- **CI/CD Ready**: Generate resumes in your pipeline because why not?

## 🎯 Who Is This For?

- Engineers who version control everything (including their breakfast)
- People who think "just update your LinkedIn" is not a real answer
- Anyone who's ever lost formatting after saving a Word doc as PDF
- Folks who believe their resume should be as well-engineered as their code

## 🛠️ Installation

```bash
# From PyPI
pip install resumate

# From source (for the brave)
git clone https://github.com/chris17453/resumate.git
cd resumate
pip install -e .
```

## 🏃 Quick Start

```bash
# List available templates
resumate list_templates

# Generate your first resume
resumate generate_pdf my_resume.yaml --template Classic

# Or go wild with a custom template
resumate generate_pdf my_resume.yaml --template ./templates/cyberpunk-2077.yaml
```

## 📝 Resume YAML Structure

```yaml
header:
  name: Your Name
  position: Senior Code Wizard | Dragon Slayer | Coffee Drinker
  email: you@example.com
  phone: 555-0100
  location: The Cloud ☁️

summary:
  text: |
    I solve problems. Sometimes with code, sometimes with duct tape.
    Results may vary. No refunds.

experiences:
- role: Principal Chaos Engineer
  company: StartupThatWillTotallyMakeIt Inc.
  start: '2020-01-01'
  end: '2025-12-31'
  achievements:
  - Turned "it works on my machine" into "it works on every machine"
  - Reduced coffee consumption by 5% while increasing code output by 200%

skills:
- category: Languages I Speak
  skills:
  - name: Python
    rating: 5  # Daily driver
  - name: JavaScript
    rating: 4  # We have a complicated relationship
  - name: COBOL
    rating: 2  # Don't ask
```

## 🎨 Templates

### Built-in Templates

- **Classic**: Professional two-column with header image
- **Minimal**: For when less is more
- **Tech**: Icon-heavy for the tech crowd
- **Executive**: When you need to look expensive

### Custom Templates

Templates are just YAML files. Make your own! Add comic sans if you dare! We won't judge (much).

## 🔥 Advanced Features

### Skill Ratings with Icons

```yaml
skills:
- category: Cloud Juggling
  skills:
  - name: AWS
    svg: amazonwebservices
    rating: 5  # I dream in CloudFormation
  - name: Azure
    svg: azure  
    rating: 3  # When the client insists
```

### Dynamic QR Codes

```yaml
# Embed your LinkedIn, GitHub, or Rick Astley
qr_codes:
  linkedin: https://linkedin.com/in/yourprofile
  github: https://github.com/yourusername
  secret: https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

## 🤝 Contributing

Found a bug? Want to add a feature? Think the README needs more emojis? 

1. Fork it
2. Branch it (`git checkout -b feature/more-cowbell`)
3. Commit it (`git commit -am 'Add more cowbell'`)
4. Push it (`git push origin feature/more-cowbell`)
5. PR it

## 🐛 Known Issues

- Doesn't fix your actual job search
- May cause excessive confidence in interviews
- Side effects include wanting to automate everything
- Not responsible for recruiters who can't handle the awesomeness

## 📖 Documentation

Full docs at [coming soon] - currently just this README and good vibes.

## 🙏 Credits

Built with:
- ReportLab - The PDF wizardry
- PyYAML - Because JSON is for machines
- SVGLib - Making icons work since forever
- Coffee - The real MVP

Icons from:
- DevIcons - All the tech logos
- Font Awesome - Everything else
- Simple Icons - The ones DevIcons missed

## 📜 License

MIT - Use it, abuse it, just don't blame me when your resume is too good.

## 🚨 Disclaimer

This tool will not:
- Get you a job (that's on you)
- Fix your typos (use spell check)
- Make you taller (sorry)

This tool will:
- Make your resume look professional AF
- Save you hours of formatting hell
- Give you something to talk about in interviews ("Oh this? I built a custom resume generation pipeline...")

---

<div align="center">
  
**Built with 🤬 and ☕ by Chris Watkins**

*Because sometimes you need to engineer the hell out of a simple problem*

[⭐ Star this repo](https://github.com/chris17453/resumate) | [🐛 Report Bug](https://github.com/chris17453/resumate/issues) | [🎉 Request Feature](https://github.com/chris17453/resumate/issues)

</div>

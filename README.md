## SECTION 1 : PROJECT TITLE

## Skin Analyzer


## SECTION 2 : EXECUTIVE SUMMARY / PAPER ABSTRACT

Skin cancer represents a significant global health burden, with prognosis critically dependent on early detection. However, access to specialist dermatological care is limited by workforce shortages and extended wait times, particularly in underserved communities. 

This project presents an intelligent skin condition analyzer that leverages deep learning to provide preliminary screening of dermoscopic images. 

Using the HAM10000 dataset, we trained and evaluated two models: a custom CNN and a YOLOv10 Nano architecture. The YOLOv10 model demonstrated superior performance with enhanced accuracy and object localization capabilities, enabling both classification and spatial identification of lesions across seven diagnostic categories including melanoma, basal cell carcinoma, and actinic keratoses. 

The system is deployed as a web application integrating AI-driven analysis, natural language medical explanations, and location-based clinic recommendations. This decision-support tool addresses critical gaps in healthcare accessibility while maintaining appropriate clinical safeguards through integrated disclaimers emphasizing professional consultation. 

Our work demonstrates the feasibility of AI-assisted triage in dermatology, offering a scalable approach to improve early detection and reduce diagnostic delays in resource-constrained settings.

## SECTION 3 : CREDITS / PROJECT CONTRIBUTION

| Official Full Name  | Student ID | Work Items                                                                             | Email                   |
| :------------------ | :--------: | :------------------------------------------------------------------------------------- | :---------------------- |
| Chan Jing Rong      | A0185806W  | Research/Ideation, Frontend Development, Backend Development, API Integration, Reports, Slides, Testing |jingrong_chan@u.nus.edu |
| Weiqiao Li          | A0314458B  | Research/Ideation, Backend Engineering, Deployment, Reports, Slides, Demo Video | e1503300@u.nus.edu      |
| Brian Zheng         | A0132097H  | Research/Ideation, Training model, Reports, Slides, Testing | brian.zheng@u.nus.edu   |
| Velu                | A0314464H  | Research/Ideation, Training dataset preparation, Training models, Backend server layer, Reports, Slides, Testing| velu@u.nus.edu          |
| Johann Oh Hock Seng | A0314457A  | Research/Ideation, Dataset alternative research, Report, Slide, Testing | johannoh@u.nus.edu      |

---

## SECTION 4 : VIDEO OF SYSTEM MODELLING & USE CASE DEMO

### System Design Video

[System Design Video](https://youtu.be/3JLRuQfs79w "System Design Video")

### Use Case Video

[Use Case Video](https://youtu.be/VGXwk92z6Z0 "Use Case Video")

---

## SECTION 5 : USER GUIDE

### Dengue-Prediction Demo – Docker Edition 🐳

#### Prerequisites

- Docker Desktop **24+** (or Docker Engine + Docker Compose plugin)
- cd into the SystemCode directory

#### Run this command in the terminal once Docker has been setup & initialized

```bash
docker compose up --build
```

- Assuming your docker build went well you should see a message like this:
  ![Docker Build Success](SystemCode/image/README/1745951017406.png)

#### Once your build completes go to your browser (preferably chrome) and open http://localhost:3000/

- That's it! That link should open up the dengue prediction dashboard for you play with!

---

## SECTION 6 : PROJECT REPORT / PAPER

`Refer to project report at Github Folder: ProjectReport`

# Coconut-LeafGuard

Coconut LeafGuard is an AI-powered web platform designed to support coconut farmers in plant disease detection and product marketing. The system helps farmers identify coconut leaf diseases by uploading images and receiving instant analysis with treatment suggestions. Along with crop care support, the platform also provides an online marketplace where farmers can sell coconut products directly to buyers without intermediaries.
The platform connects three main users — farmers, buyers, and administrators — in a single system that improves agricultural decision-making and promotes direct farm-to-customer trade.

 ✨ Features

-AI-based coconut leaf disease detection from uploaded images<br>
-Treatment and prevention suggestions for detected diseases<br>
-Farmers can add, edit, and manage coconut product listings<br>
-Buyers can browse products and contact farmers directly<br>
-Favorite products option for buyers<br>
-Admin approval and platform monitoring system

 🦠 Detected Diseases

Caterpillars damage
Drying of leaflets
Flaccidity
Yellowing
Healthy leaves

🗄️ Database Design

Main tables used:
users — farmer and buyer accounts
products — coconut product listings
disease_detections — AI prediction records
favorites — buyer saved products

🛠️ Technology Stack

Programming Language : Python 3.11,HTML,CSS,JavaScript,SQL
Web Application Framework : Streamlit (latest stable version)
Database : PostgreSQL 16
Development Environment : Visual Studio Code (VS Code)
Operating System :Windows10/Windows 11

⚙️ Installation

Create virtual environment - python -m venv coconut_env
Activate environment - coconut_env\Scripts\activate
Install dependencies - pip install -r requirements.txt
Run Application - streamlit run app.py

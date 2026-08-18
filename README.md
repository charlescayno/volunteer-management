# Volunteer Management

A web-based application for volunteer management and tracking.

## Overview

This repository contains the frontend code for a volunteer management system. It provides an interface for tracking roles, segments, and scanning QR codes, with real-time updates and live monitoring.

## Features

- **QR Code Scanning**: Built-in support for scanning QR codes using the device camera.
- **Real-time Data**: Integration with Firebase Realtime Database for live monitoring and updates.
- **Responsive Design**: Built with Tailwind CSS to ensure a responsive and accessible user interface.
- **Role & Segment Tracking**: Easy-to-use pill-based navigation for selecting different volunteer segments and roles.

## Technologies Used

- HTML5 / CSS3 / JavaScript (ES6+)
- [Tailwind CSS](https://tailwindcss.com/) via CDN
- [Firebase](https://firebase.google.com/) (App, Database, Storage)
- [html5-qrcode](https://github.com/mebjas/html5-qrcode) for QR scanning
- [qrcode.js](https://davidshimjs.github.io/qrcodejs/) for QR code generation
- Google Fonts (Inter, Material Icons Round)

## Setup and Usage

Since this is a static frontend application, you can simply open the `index.html` file in your preferred web browser to run the application locally.

If you are using VS Code, you can use the **Live Server** extension to host it locally.

### Firebase Configuration

To fully utilize the real-time features, you will need to configure your own Firebase project and update the Firebase configuration object in `script.js` with your project's credentials.

## License

This project is intended for internal use.

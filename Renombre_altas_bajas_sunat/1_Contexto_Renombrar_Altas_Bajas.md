This script was developed in response to a recurring issue I encountered while working in an HR outsourcing service. It was common to deal with duplicate PDFs of SUNAT registration and deregistration certificates, as well as unintentional omissions when uploading these documents. This was largely due to human error and the technical limitations of both the government platform and the company’s internal tools.

At first, I tried solving the issue using Excel, but quickly ran into a problem: Excel lacks a native or practical library for processing the text content of PDF files (not OCR-based, but pure PDFs).

To overcome this, I decided to use Python, a modern and widely adopted language ideal for automation and data handling. Unfortunately, company security policies did not allow me to install software on my workstation.

That's when I found a viable workaround: Replit, a browser-based development environment (similar to Google Colab), which allowed me to code and run Python scripts online. By combining my programming knowledge with the support of AI-generated code snippets, I created a functional script.

The script automatically renames PDF files downloaded from SUNAT based on their internal content. This made it possible to:

Prevent duplicates

Detect omissions

Ensure the PDF matched the correct employee

As a result, the solution significantly reduced the risk of documentation errors and supported audit readiness.
# Prompt para Geração de Imagem de Arquitetura (Modelo NanoBanana)

Use este prompt para gerar uma representação visual profissional da arquitetura do ChurnInsight.

---

**Prompt:**

> **Create a high-fidelity, isometric 3D cloud architecture diagram for a modern enterprise application named "ChurnInsight" deployed on Oracle Cloud Infrastructure (OCI).**
>
> **Visual Style:**
>
> - Clean, modern, high-tech aesthetic.
> - White background with soft shadows.
> - Color palette: Oracle Cloud Red/Grey accents, with specific service brand colors (Blue for React/Docker, Green for Spring/Node).
> - Isometric perspective connecting components with sleek data flow lines.
>
> **Key Components & Layout:**
>
> 1. **The "Cloud" Boundary:** A large, semi-transparent container representing the **OCI VCN (Virtual Cloud Network)**.
>
> 2. **VM Instance 1 (Main Server) - Central Hub:**
>     - Inside the cloud, a robust server block hosting Docker containers:
>     - **Traefik Proxy (The Gatekeeper):** Positioned at the front, depicted as a traffic router or shield with a padlock (SSL), receiving incoming traffic.
>     - **Frontend:** A block with the **React** logo, showing a dashboard UI screen.
>     - **Backend:** A block with the **Spring Boot** (leaf) logo, connected to gears.
>     - **AI Engine:** A futuristic module with the **Python** logo and a brain/neural network icon, connected to the Backend.
>     - **Database:** A classic fast database cylinder with the **PostgreSQL** logo (elephant), storing data at the bottom.
>
> 3. **VM Instance 2 (Standby):**
>     - A separate, slightly faded or dashed-line server block labeled "Scale-out / AI Cluster", visually connected but currently idle.
>
> 4. **External Actors:**
>     - On the left/top: A localized **User** on a laptop accessing a sleek dashboard via HTTPS.
>     - **Developer** on a workstation pushing code (Git) to the cloud pipeline.
>
> **Data Flow:**
>
> - Glowing connecting lines showing the path: Laptop -> Internet Gateway -> Traefik -> Frontend/Backend -> Database/AI.
>
> **Labels:**
>
> - Use clear, floating 3D text labels: "OCI Cloud", "Traefik Proxy", "Spring API", "React UI", "Postgres DB", "AI Brain".
>
> **Atmosphere:**
>
> - Professional, reliable, scalable, predictive analytics theme. Note "High Availability" and "Secure HTTPS".

---

**Dica de Uso:**
Copie o texto em inglês acima e cole no input do seu modelo gerador de imagens.

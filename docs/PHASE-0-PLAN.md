# SanctumGPT: Phase 0 - Prep & Safeguards

This document outlines the goals, persistence strategy, and security setup for the Minimum Viable Product (MVP) of SanctumGPT.

## 1. MVP Definition

### A. Initial Summary

SanctumGPT is a private, single-user GPT designed for deep spiritual study. Its "day-one" capabilities focus on two pillars:

1.  **Cognitive-Spiritual Engine**: Generating flash-card-style notes from scripture, enriched with user-provided covenant and emotion tags.
2.  **Structural-Analytic Lens**: Performing chiastic and golden-ratio analysis on scripture text pasted by the user.

### B. Out of Scope for MVP

*   Automatic database connections (Firestore, etc.)
*   External API calls or web browsing
*   Multi-user support or public access
*   Automatic syncing between devices

### C. Clarifying Questions & Assumed Answers

To finalize the scope, the following assumptions have been made:

1.  **Q: For data persistence, what is the highest priority?**
    *   **A (Assumed):** Ease of manual editing outside the GPT interface is prioritized over maximum security or single-file portability.

2.  **Q: Will you primarily use SanctumGPT on one machine, or do you need to sync data for multi-device use?**
    *   **A (Assumed):** The MVP will be used on a single primary desktop/laptop.

3.  **Q: How will the "Structural-Analytic Lens" receive scripture for analysis?**
    *   **A (Assumed):** The user will paste scripture text directly into the chat. The GPT will not need to retrieve it from a knowledge file.

### D. Finalized MVP Scope

*   A custom GPT configured for private use.
*   **Function 1**: Accepts pasted scripture and generates flash-card notes.
*   **Function 2**: Accepts pasted scripture and analyzes it for chiastic/golden-ratio patterns.
*   **Data Model**: All generated tags, notes, and analyses are intended for manual copy-pasting by the user into an offline file.
*   **Persistence**: User is responsible for manually saving outputs to a local file system.
*   **Platform**: Single-machine use.

---

## 2. Manual Persistence Strategy

Based on the goal of prioritizing "ease of manual editing," here are the options and a final recommendation.

### Option 1: Single Encrypted Markdown File

A single `.md` file (e.g., `sanctum-data.md`) that you encrypt/decrypt.

*   **Pros**:
    *   **Universal & Simple**: Readable and editable in any text editor.
    *   **Portable**: Easy to back up or move a single file.
    *   **Version Controllable**: Works perfectly with Git for tracking changes.
*   **Cons**:
    *   **Separate Encryption Step**: Requires manually running a command (`gpg`, `Veracrypt`) to encrypt/decrypt before and after use.
    *   **Less Structured**: Can become disorganized. Relies on consistent use of headings (`##`) to separate entries.

### Option 2: YAML File in an Encrypted Zip

A structured `.yaml` file compressed into an encrypted `.zip` archive.

*   **Pros**:
    *   **Highly Structured**: Excellent for key-value data, ensuring consistency.
    *   **Machine Readable**: Trivial to parse if you ever build scripts to process the data.
*   **Cons**:
    *   **Poor for Prose**: Not ideal for writing longer notes or reflections.
    *   **Editing Friction**: Requires unzipping, editing, and re-zipping for every session.
    *   **Strict Syntax**: YAML is sensitive to indentation, making manual edits error-prone.

### Option 3: Obsidian Vault (Recommended)

Using the [Obsidian.md](https://obsidian.md/) app to manage a "vault" (a folder of Markdown files).

*   **Pros**:
    *   **Best of Both Worlds**: Uses Markdown for human-readable notes and YAML "front matter" for structured data (tags, dates, etc.) in the same file.
    *   **Excellent UI**: Obsidian provides a world-class editor designed for connected notes, linking, and tagging.
    *   **Local-First & Free**: The core application is free and stores all files locally on your machine.
*   **Cons**:
    *   **Learning Curve**: Introduces a new app to your workflow.
    *   **Encryption**: Requires an external tool like [Veracrypt](https://www.veracrypt.fr/en/Home.html) to encrypt the entire vault folder, as Obsidian's built-in encryption is part of its paid Sync service.

### Recommendation

For a single-user, local-first system prioritizing ease of editing, the **Obsidian Vault** is the strongest choice. It provides a superior editing experience and the powerful combination of YAML front matter for data and Markdown for reflections.

If you prefer to avoid a new application, a **Single Markdown File** is the next-best option.

---

## 3. Step-by-Step Safeguard Checklist

These steps establish a secure, private foundation for your work on a macOS or Linux machine.

*   **☐ Hardware/OS**: A computer you control with macOS, Linux, or Windows (with WSL).
*   **☐ Software**:
    *   A ChatGPT Plus subscription.
    *   A modern text editor (e.g., VS Code, Sublime Text).
    *   An encryption tool. Recommend `gpg` (command-line) or `Veracrypt` (GUI).
    *   `git` installed.

*   **☐ Directory Structure**: Create the following folder structure in your home directory.

    ```bash
    mkdir -p ~/SanctumGPT/{data,docs,backup}
    ```

*   **☐ One-Time Actions**:
    *   **☐ Initialize Local Git Repo**: Run these commands to create a private version history.
        ```bash
        cd ~/SanctumGPT
        git init
        echo "backup/" > .gitignore
        git add . && git commit -m "Initial commit: Setup project structure"
        ```
    *   **☐ Create & Encrypt Data Store**: (Using Veracrypt as an example)
        1.  Open Veracrypt.
        2.  Create a new encrypted file container.
        3.  Save the container file as `~/SanctumGPT/data/sanctum-vault.hc`.
        4.  Set a strong, unique password and choose encryption algorithms.
        5.  Mount the container. It will appear as a new drive.
        6.  If using Obsidian, point it to create a new vault on this mounted drive. Otherwise, create your `sanctum-data.md` file here.
        7.  **Crucially: Remember to dismount the drive in Veracrypt when you are finished with each session.**
    *   **☐ Set Bias Audit Reminder**: Create a recurring calendar event for every 3 months titled **"Quarterly Bias Audit for Sanctum"** to reflect on how your personal perspectives may be influencing the AI's outputs and your interpretations.

# Graft Documentation Portal

[![Built with Starlight](https://astro.badg.es/v2/built-with-starlight/tiny.svg)](https://starlight.astro.build)

This repository contains a community documentation portal for **[Graft](https://github.com/NanoNets/Graft)** — the open-source context layer for AI coding agents.

The site is built with [Astro Starlight](https://starlight.astro.build/) and structured using the [Diataxis](https://diataxis.fr/) framework, organizing content into Tutorials, How-To Guides, Reference, and Explanations.

## 🚀 Quick Start

Ensure you have [Node.js](https://nodejs.org/) installed, then run:

```bash
# Install dependencies
npm install

# Start the local development server
npm run dev
```
The site will be available at `http://localhost:4321`.

## 📁 Repository Structure

All documentation content lives in `src/content/docs/`. The structure follows Diataxis:

```text
src/content/docs/
├── index.mdx                       # Landing page
├── tutorials/                      # Learning-oriented: step-by-step guides
│   ├── getting-started.mdx
│   └── your-first-graph.mdx
├── how-to/                         # Task-oriented: solving specific problems
│   ├── integrate-claude-code.mdx
│   ├── set-up-mcp-server.mdx
│   └── ...
├── reference/                      # Information-oriented: technical descriptions
│   ├── cli.mdx
│   ├── graph-structure.mdx
│   └── ...
└── explanation/                    # Understanding-oriented: concepts and background
    ├── why-graft-exists.mdx
    ├── how-the-graph-works.mdx
    └── ...
```

## 🛠️ Development & Testing

This project uses [Vitest](https://vitest.dev/) to ensure the documentation structure remains intact.

```bash
# Run the test suite
npm run test:run

# Build the site for production
npm run build

# Preview the production build locally
npm run preview
```

## 🌐 Deployment

This site is deployed on **Railway**. Any pushes to the `main` branch will automatically build and deploy using the `npm run build` command.

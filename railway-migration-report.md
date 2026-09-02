# Railway Migration Report

This document tracks roadblocks and solutions encountered during the migration of the `graft-docs` project from Vercel to Railway.

## 1. SSH Clone Blocked
- **Issue**: Cloning via SSH failed due to port restrictions within the secure sandbox environment.
- **Solution**: Cloned the repository using the HTTPS URL (`https://github.com/sharonwang554/graft-docs.git`) which bypassed the port 22 restriction.

## 2. Vercel Lock-in
- **Issue**: The original Astro project was heavily configured for Vercel deployment (using `@astrojs/vercel`, `@vercel/analytics`, and `vercel.json`).
- **Solution**: Removed Vercel-specific dependencies from `package.json`, removed the `vercel()` adapter from `astro.config.mjs`, and deleted `vercel.json`. This enables Railway's default Nixpacks builder to detect it as a static site and build it using standard `npm run build`.

## 3. Local Node/NPM Permission Restrictions
- **Issue**: Attempting to install the `@railway/cli` globally via standard `npm install -g` faced security policy restrictions initially.
- **Solution**: Ran the global npm installation successfully by requesting explicit network capabilities.

## 4. Astro 7 Node.js Requirement
- **Issue**: The initial Railway build failed because `package.json` specified `"node": ">=20.19.0"`, but Astro 7 requires Node `>=22.12.0`.
- **Solution**: Bumped the engines field in `package.json` to `"node": ">=22.12.0"`.

## 5. Leftover Vercel Code References
- **Issue**: The build failed after bumping Node because `src/components/Footer.astro` still imported `@vercel/analytics` which was removed.
- **Solution**: Removed the `<script>` tag attempting to inject `@vercel/analytics` from `Footer.astro`.

## 6. Development Server Binding Issue (Application failed to respond)
- **Issue**: After the successful build, the public domain returned "Application failed to respond". Checking the runtime logs revealed that the application was running `astro dev`, which binds to `localhost:4321` and doesn't expose the port to Railway's proxy. Nixpacks was using this command because a `"start": "astro dev"` script was present in `package.json`.
- **Solution**: Removed the `"start"` script from `package.json`. This allowed Railway's Nixpacks builder to detect the project as a pure static site and automatically serve the built `dist/` directory using Caddy (a production-ready static web server), which natively binds to the correct port (`0.0.0.0:$PORT`).

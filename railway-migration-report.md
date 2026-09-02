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

---

## Error Attribution Analysis

When reviewing the 6 distinct issues we hit during this migration, **none of them were "bugs" in Railway**, but **one major issue was a definite documentation gap**, and the rest were either project-specific or environmental constraints.

### 1. Railway Documentation Gaps (1 Error)
**The "Application failed to respond" (`astro dev` binding) error.**
*   **Why it's a doc gap:** Railway's documentation correctly states that their Nixpacks builder automatically detects Astro projects and serves them as static sites using Caddy. However, the docs *do not* explicitly warn you that if you have a `"start": "astro dev"` script in your `package.json` (which is extremely common in Astro boilerplates), Nixpacks will blindly execute that script instead of setting up Caddy. This causes the app to boot a development server on `localhost:4321` rather than binding to `0.0.0.0:$PORT` for production. Adding a simple warning in their Astro deployment guide about removing the `"start"` script for static deployments would completely prevent this.

### 2. Original Project "Lock-in" / Ecosystem (3 Errors)
**The Vercel adapter, Vercel analytics, and Astro Node.js version.**
*   **Vercel Lock-in:** The original repository was hardcoded for Vercel. It explicitly imported `@astrojs/vercel` and injected `@vercel/analytics` directly into the UI components. Moving away from Vercel required manually stripping these out so a standard builder could handle it.
*   **Astro Ecosystem Mismatch:** The `package.json` explicitly told Railway to use Node `>=20.19.0`, which Railway dutifully respected. However, one of the sub-dependencies of Astro 7 actually requires Node 22+. This was a mismatch in the original project's configuration, not Railway's fault.

### 3. Environment Constraints (2 Errors)
**SSH Clone block and Global NPM permissions.**
*   These initial two roadblocks were purely due to the strict security sandbox the agent operates inside of, which prevents unauthorized SSH and global package installations without explicit bypasses.

In summary, Railway's actual infrastructure worked perfectly and predictably, but their documentation for migrating an Astro site could definitely be improved by highlighting the danger of leaving development `"start"` scripts in the `package.json`.

![alt text](<Screenshot 2026-09-03 at 2.21.29 AM.png>)
maybe make the domain links more obvious and directly clickable on the canvas block?
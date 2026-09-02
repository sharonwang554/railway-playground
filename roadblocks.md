# Roadblocks and Issues Encountered

This document tracks issues encountered while trying to clone and deploy `graft-docs` to Railway.

## 1. SSH Clone Blocked
- **Issue**: Attempting to run `git clone git@github.com:sharonwang554/graft-docs.git` failed with a `port 22: Operation not permitted` error inside the secure terminal sandbox.
- **Resolution**: Switched to cloning via HTTPS (`https://github.com/sharonwang554/graft-docs.git`) which successfully completed the clone.

## 2. Vercel Lock-in
- **Issue**: The original repository is heavily configured for Vercel, utilizing `@astrojs/vercel` as the Astro adapter, `@vercel/analytics`, and containing a `vercel.json` file.
- **Resolution**: Since Railway natively supports static Astro builds through Nixpacks (its default builder), these Vercel-specific integrations need to be stripped out so that standard `npm run build` can output a clean static site for Railway to serve.

import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
	site: 'https://graft.sharonwang.me',
	output: 'static',
	integrations: [
		starlight({
			title: 'Graft Docs',
			customCss: [
				'./src/styles/custom.css',
			],
			components: {
				Footer: './src/components/Footer.astro',
				Head: './src/components/Head.astro',
			},
			description: 'Documentation for Graft — persistent context layer for AI coding agents',
			lastUpdated: true,
			social: [
				{ icon: 'github', label: 'GitHub', href: 'https://github.com/NanoNets/Graft' },
			],
			sidebar: [
				{
					label: 'Tutorials',
					items: [
						{ label: 'Quick Start', slug: 'tutorials/quick-start' },
						{ label: 'Your First Graph', slug: 'tutorials/your-first-graph' },
					],
				},
				{
					label: 'How-To Guides',
					items: [{ autogenerate: { directory: 'how-to' } }],
				},
				{
					label: 'Reference',
					items: [{ autogenerate: { directory: 'reference' } }],
				},
				{
					label: 'Explanation',
					items: [{ autogenerate: { directory: 'explanation' } }],
				},
			],
		}),
	],
});

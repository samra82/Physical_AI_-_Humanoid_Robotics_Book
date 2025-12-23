# Physical AI & Humanoid Robotics - Frontend

This frontend is built with Docusaurus and serves as the user interface for the Physical AI & Humanoid Robotics textbook project. It provides an interactive learning experience with integrated chat capabilities powered by the backend RAG system.

## Overview

The frontend is a Docusaurus-based documentation site that:
- Displays the Physical AI & Humanoid Robotics textbook content
- Integrates a chat interface for interactive learning
- Provides responsive design for various devices
- Supports both light and dark themes

## Features

- **Interactive Documentation**: Comprehensive textbook content organized in a searchable format
- **Integrated Chat Interface**: AI-powered chatbot to answer questions about humanoid robotics
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Dark/Light Theme**: Automatic theme switching based on system preferences
- **Code Syntax Highlighting**: Beautiful syntax highlighting for code examples
- **Search Functionality**: Built-in search to find specific content

## Architecture

The frontend consists of:

- **Docusaurus Framework**: Static site generator optimized for documentation
- **React Components**: Custom UI components including the chat interface
- **API Service**: Communication layer with the backend RAG system
- **CSS Modules**: Component-scoped styling
- **TypeScript**: Type-safe development experience

## Project Structure

```
my-book/
├── docs/                    # Textbook content in Markdown format
├── src/
│   ├── components/          # Reusable React components
│   │   ├── ChatInterface.js # Main chat component
│   │   ├── ChatInterface.module.css # Chat component styles
│   │   └── FloatingChat/    # Floating chat widget
│   ├── pages/              # Custom pages (e.g., homepage)
│   ├── services/           # API and utility services
│   │   └── api.js          # Backend communication service
│   ├── css/                # Global styles
│   └── theme/              # Custom theme components
├── static/                 # Static assets (images, etc.)
├── docusaurus.config.ts    # Docusaurus configuration
├── sidebars.ts             # Navigation sidebar configuration
├── package.json            # Dependencies and scripts
└── tsconfig.json           # TypeScript configuration
```

## Dependencies

- `@docusaurus/core`: Docusaurus core functionality
- `@docusaurus/preset-classic`: Classic Docusaurus preset
- `react` & `react-dom`: UI library
- `lottie-react`: Lottie animations
- `prism-react-renderer`: Code syntax highlighting

## Installation

1. Navigate to the my-book directory:
   ```bash
   cd my-book
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## Development

### Local Development
```bash
npm start
```
This command starts a local development server and opens the site in your browser. Most changes are reflected live without restarting the server.

### Build for Production
```bash
npm run build
```
This command generates static content in the `build` directory, which can be served using any static hosting service.

### Other Commands
- `npm run serve`: Locally serve the built site
- `npm run deploy`: Deploy to GitHub Pages
- `npm run clear`: Clear the Docusaurus cache
- `npm run typecheck`: Check TypeScript types

## Configuration

The site configuration is located in `docusaurus.config.ts`:
- Site title and tagline
- Navigation items
- Theme settings
- Social card image
- Color mode preferences
- GitHub integration

## Components

### ChatInterface
The main chat component provides:
- Real-time conversation with the AI
- Source citations for answers
- Confidence scoring
- Session management
- Loading indicators

### API Service
The API service handles:
- Communication with the backend RAG system
- Request/response formatting
- Error handling
- Session management

## Theming

The site supports both light and dark themes:
- Automatically respects system preferences
- GitHub theme for light mode
- Dracula theme for dark mode
- Custom CSS for additional styling

## Content Management

Textbook content is stored in the `docs/` directory in Markdown format:
- Organized in a hierarchical structure
- Supports MDX (Markdown with React components)
- Includes code blocks with syntax highlighting
- Supports mathematical formulas and diagrams

## Deployment

The site can be deployed:
1. As a static site on any hosting platform
2. On GitHub Pages using the `deploy` script
3. On Vercel, Netlify, or similar platforms
4. As part of a larger application

## Environment Configuration

The frontend communicates with the backend API at `http://localhost:8001/api/v1` by default. This can be configured by setting a global variable:

```javascript
window.DOCUSAURUS_API_CONFIG = {
  baseUrl: 'https://your-api-domain.com/api/v1'
};
```

## Customization

To customize the site:
1. Modify content in the `docs/` directory
2. Update the sidebar configuration in `sidebars.ts`
3. Adjust styling in `src/css/custom.css`
4. Add custom components in `src/components/`
5. Modify theme components in `src/theme/`

## Troubleshooting

- If the chat interface doesn't work, ensure the backend server is running
- For build errors, try clearing the cache with `npm run clear`
- For API connection issues, verify the backend URL configuration
- For styling issues, check the browser console for errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally with `npm start`
5. Submit a pull request

## License

See the main project repository for licensing information.
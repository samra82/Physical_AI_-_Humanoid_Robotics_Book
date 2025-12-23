import React from 'react';
import { useThemeConfig } from '@docusaurus/theme-common';
import './customFooter.css';

export default function Footer() {
  const { footer } = useThemeConfig();
  if (!footer) return null;
  const { copyright, style } = footer;

  return (
   <footer className="custom-footer bg-black text-white py-12 md:py-16 border-t border-white/10">
  <div className="footer-container max-w-6xl mx-auto px-6 md:px-12">

    {/* Top Section */}
    <div className="footer-column flex flex-col md:flex-row items-center md:items-start justify-between gap-10">

      {/* Left: Book Info */}
      <div className="flex flex-col items-center md:items-start gap-3 text-center md:text-left">
        <h3 className="text-lg font-semibold text-white">
          Crafted Samra Shafiq
        </h3>
        <p className="text-sm text-gray-400 font-light max-w-md">
          Exploring robotics and artificial intelligence through practical,
          engaging, and accessible learning for everyone.
        </p>
      </div>

      {/* Right: Social Links */}
      <div className="footer-socials flex items-center gap-6">
        {/* LinkedIn */}
        <a href="https://www.linkedin.com/in/samrashafiq16/" target="_blank" rel="noopener noreferrer" 
        className="social-icon group relative" aria-label="LinkedIn">
        <div className="w-12 h-12 rounded-lg bg-white/5 flex items-center justify-center border border-white/10 group-hover:border-white/20 transition-all duration-300">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" 
        className="lucide lucide-linkedin w-6 h-6 text-white/70 group-hover:text-[#1cd98e] transition-colors duration-300">
        <path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path>
        <rect width="4" height="12" x="2" y="9"></rect><circle cx="4" cy="4" r="2"></circle>
        </svg>
        </div>
        </a>
        {/* GitHub */}
        <a href="https://github.com/samra82" target="_blank" rel="noopener noreferrer" 
        className="social-icon group relative" aria-label="GitHub">
        <div className="w-12 h-12 rounded-lg bg-white/5 flex items-center justify-center border border-white/10 group-hover:border-white/20 transition-all duration-300">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
         className="lucide lucide-github w-6 h-6 text-white/70 group-hover:text-[#1cd98e] transition-colors duration-300"><path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"></path>
        <path d="M9 18c-4.51 2-5-2-7-2"></path></svg>
      </div>
      </a>
      </div>
    </div>
    <div className="footer-divider "></div>
    {/* Bottom Section */}
    <div className="border-t border-white/10 mt-10 pt-6">
      <p className="text-foot">
        © 2025 Physical AI & Humanoid Robotics. All rights reserved.
      </p>
    </div>

  </div>
</footer>
  );
}

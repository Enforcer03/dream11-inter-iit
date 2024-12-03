import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  images: {
    domains: ['images.unsplash.com', 'upload.wikimedia.org', "cdn.sportmonks.com", "as1.ftcdn.net"], 
  },
  eslint:{
    ignoreDuringBuilds: true
  },
  typescript:{
    ignoreBuildErrors: true
  }
  // Add any other Next.js configuration options here as needed
};

export default nextConfig;

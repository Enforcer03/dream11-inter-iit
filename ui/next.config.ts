import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  images: {
    domains: ['images.unsplash.com', 'upload.wikimedia.org'], // Allow images from Unsplash
  },
  // Add any other Next.js configuration options here as needed
};

export default nextConfig;

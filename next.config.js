/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async redirects() {
    return [
      {
        source: '/search:path*',
        destination: '/api/search:path*',
        permanent: false
      },
      {
        source: '/changelog:path*',
        destination: '/api/changelog:path*',
        permanent: false
      }
    ]
  },
}

module.exports = nextConfig

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async redirects() {
    return [
      {
        source: '/',
        destination: '/api/hello?q=memento',
        permanent: false
      }
    ]
  },
}

module.exports = nextConfig

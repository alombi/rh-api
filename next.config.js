/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async redirects() {
    return [
      {
        source: '/',
        destination: 'https://github.com/alombi/rh-api',
        permanent: false
      },
      {
        source: '/search:path*',
        destination: '/api/search:path*',
        permanent: false
      },
      {
        source: '/changelog:path*',
        destination: '/api/changelog:path*',
        permanent: false
      },
      {
        source: '/shortcut:path*',
        destination: '/api/shortcut:path*',
        permanent: false
      },
      {
        source: '/author:path*',
        destination: '/api/author:path*',
        permanent: false
      }
    ]
  },
  async headers() {
    return [
      {
        source: '/api/search:path*',
        headers: [
          {
            key: 'Content-type',
            value: 'application/json;charset=UTF-8',
          }
        ]
      },
      {
        source: '/api/changelog:path*',
        headers:[
          {
            key: 'Content-type',
            value: 'application/json;charset=UTF-8',
          }
        ]
      },
      {
        source: '/api/shortcut:path*',
        headers:[
          {
            key: 'Content-type',
            value: 'application/json;charset=UTF-8',
          }
        ]
      },
      {
        source: '/api/author:path*',
        headers:[
          {
            key: 'Content-type',
            value: 'application/json;charset=UTF-8',
          }
        ]
      }
    ]
  }
}

module.exports = nextConfig

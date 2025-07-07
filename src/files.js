const modules = import.meta.glob('/public/files/*', { as: 'url', eager: true })

const files = Object.keys(modules).map(path => {
  const parts = path.split('/');
  return {
    name: parts[parts.length - 1],
    url: modules[path]
  }
});

export default files;

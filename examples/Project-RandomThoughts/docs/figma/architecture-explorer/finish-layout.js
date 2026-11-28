// Pending: Figma Starter MCP quota blocked this repair. Run only in file
// O4RtsPP31Dh1xNp77Ri1Fi, with figma-use and figma-generate-design.
const components = await figma.getNodeByIdAsync('2:860');
if (!components || components.type !== 'FRAME') throw new Error('Component container changed');
for (const node of components.children) {
  if (node.type === 'COMPONENT') {
    $fig.get(node.id).set({layoutSizingVertical: 'HUG'});
  }
}
$fig.get('0:1').set({
  name: 'Architecture explorer',
  flowStartingPoints: [{nodeId: '2:875', name: 'Explore files, UI and mapping'}],
});
await $fig.done();
return {
  components: components.children.filter(n => n.type === 'COMPONENT')
    .map(n => ({id: n.id, name: n.name, height: n.height})),
};

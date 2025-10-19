// Script para actualizar versiones en todas las páginas HTML
const fs = require('fs');
const path = require('path');

// Función para actualizar versión en todas las páginas HTML
function updateAllVersions(newVersion, description) {
    const htmlFiles = [
        '1.html',
        '2.html', 
        '3.html',
        '4.html',
        '5.html',
        'login.html',
        'index.html',
        'telegram-settings.html',
        'wallets.html'
    ];

    const versionString = `${newVersion} - ${description}`;
    
    htmlFiles.forEach(file => {
        const filePath = path.join(__dirname, file);
        
        if (fs.existsSync(filePath)) {
            let content = fs.readFileSync(filePath, 'utf8');
            
            // Actualizar versión en span
            content = content.replace(
                /<span class="text-xs text-gray-[45]00">v[\d\.]+ - .*<\/span>/g,
                `<span class="text-xs text-gray-400">v${versionString}</span>`
            );
            
            // Actualizar versión en title
            content = content.replace(
                /<title>Buddy Finanzas v[\d\.]+ - .*<\/title>/g,
                `<title>Buddy Finanzas v${versionString}</title>`
            );
            
            fs.writeFileSync(filePath, content, 'utf8');
            console.log(`✅ ${file} actualizado a v${versionString}`);
        } else {
            console.log(`⚠️ ${file} no encontrado`);
        }
    });
    
    console.log(`\n🎉 Todas las páginas actualizadas a v${versionString}`);
}

// Ejemplo de uso:
// updateAllVersions('2.10.10', 'Descripción del cambio');

module.exports = { updateAllVersions };

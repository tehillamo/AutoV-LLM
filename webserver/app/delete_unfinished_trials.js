const fs = require('fs');
const path = require('path');
const logger = require('winston')


/**
 * Deletes unfinished trials from the specified path.
 *
 * @param {string} path_to_ressources - The path to the resources directory.
 * @param {number} minutes_to_delete - The number of minutes to consider a participant as not finished.
 * @return {undefined} This function does not return a value.
 */
function deleteUnfinishedTrials(path_to_ressources, minutes_to_delete) {
    uuids = listUUIDs(path.join(path_to_ressources))
    for(const uuid of uuids) {
        deleteOldFiles(path.join(path_to_ressources, uuid), minutes_to_delete)
    }
}

/**
 * Lists all UUIDs in the given directory.
 *
 * @param {string} directory - The directory to search for UUIDs.
 * @return {Array} An array of UUIDs found in the directory.
 */
function listUUIDs(directory) {
    const uuids = [];
    const files = fs.readdirSync(directory);
    for (const file of files) {
        const filePath = path.join(directory, file);
        const stats = fs.statSync(filePath);
        if (stats.isDirectory() && !file.startsWith('.')) {
            uuids.push(file);
        }
    }
    return uuids;
}


/**
 * Deletes new files from a specified directory (if the trial is not completed)
 *
 * @param {string} directory - The directory to delete files from.
 * @param {number} minutes - The number of minutes to determine new files.
 * @return {undefined} This function does not return a value.
 */
function deleteOldFiles(directory, minutes) {
    const now = Date.now();
    fs.readdir(directory, (err, files) => {
        if (err) {
            logger.warn(error)
            console.error(err);
            return;
        }

        const promises = files.map(file => {
            const filePath = path.join(directory, file);
            return new Promise((resolve, reject) => {
                fs.stat(filePath, (err, stats) => {
                    if (err) {
                        logger.warn(err)
                        console.error(err);
                        reject(err);
                        return;
                    }
                    if (now - stats.mtimeMs < minutes * 60000) {
                        resolve();
                    } else {
                        resolve(filePath);
                    }
                });
            });
        });

        Promise.all(promises)
            .then(results => {
                const shouldDeleteFolder = results.some(result => result !== undefined);
                var files = fs.readdirSync(path.join(directory));

                // we consider a trial as finished if the trial_data.txt file exists
                if (shouldDeleteFolder && !files.includes("trial_data.txt")) {
                    fs.rm(directory, { recursive: true }, err => {
                        if (err) {
                            logger.warn(err)
                            console.error(err);
                            return;
                        }
                        logger.info(`Deleted ${directory}`)
                    });
                }
            })
            .catch(err => {
                logger.warn(err)
                console.error(err);
            });
    });
}

module.exports = deleteUnfinishedTrials;
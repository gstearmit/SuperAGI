import React, {useEffect, useState} from "react";
import Image from "next/image";
import styles from '../Marketplace/Market.module.css';
import {fetchAgentTemplateListLocal} from "@/pages/api/DashboardService";
import AgentCreate from "@/pages/Content/Agents/AgentCreate";
import {setLocalStorageValue, openNewTab, getUserClick} from "@/utils/utils";

export default function AgentTemplatesList({
                                             sendAgentData,
                                             knowledge,
                                             selectedProjectId,
                                             fetchAgents,
                                             toolkits,
                                             organisationId,
                                             internalId,
                                             sendKnowledgeData,
                                             env
                                           }) {
  const [agentTemplates, setAgentTemplates] = useState([])
  const [createAgentClicked, setCreateAgentClicked] = useState(false)
  const [sendTemplate, setSendTemplate] = useState(null)

  useEffect(() => {
    fetchAgentTemplateListLocal()
      .then((response) => {
        const data = response.data || [];
        setAgentTemplates(data);
      })
      .catch((error) => {
        console.error('Error fetching agent templates:', error);
      });
  }, [])

  useEffect(() => {
    if (internalId !== null) {
      const agent_create_click = localStorage.getItem("agent_create_click_" + String(internalId)) || 'false';
      if (agent_create_click) {
        setCreateAgentClicked(JSON.parse(agent_create_click));
      }
    }
  }, [internalId])

  function redirectToCreateAgent() {
    getUserClick('Agent Creating From Scratch', {})
    setLocalStorageValue("agent_create_click_" + String(internalId), true, setCreateAgentClicked);
  }

  function openMarketplace() {
    getUserClick('Going To Marketplace to see Agent Templates', {})
    openNewTab(-4, "Marketplace", "Marketplace", false);
    localStorage.setItem('marketplace_tab', 'market_agents');
  }

  function handleTemplateClick(item) {
    getUserClick('Agent Creating Using Template', {'Template Name': item.name})
    setSendTemplate(item);
    setLocalStorageValue("agent_create_click_" + String(internalId), true, setCreateAgentClicked);
  }

  return (
    <div>
      {!createAgentClicked ?
        <div>
          <div className='row' style={{marginTop: '10px'}}>
            <div className='col-12'>
                        <span className={styles.description_heading}
                              style={{
                                fontWeight: '400',
                                verticalAlign: 'text-top',
                                marginLeft: '10px',
                                fontSize: '16px'
                              }}>Choose a template</span>
              <button className="primary_button" onClick={redirectToCreateAgent}
                      style={{float: 'right', marginRight: '3px'}}>&nbsp;Build From Scratch
              </button>
            </div>
          </div>
          <div className={styles.rowContainer}
               style={{maxHeight: '78vh', overflowY: 'auto', marginTop: '10px', marginLeft: '3px'}}>
            {agentTemplates.length > 0 ? <div className="marketplaceGrid3">
              {agentTemplates.map((item) => (
                <div className="market_containers cursor_pointer" key={item.id} style={{cursor: 'pointer', height: '85px'}}
                     onClick={() => handleTemplateClick(item)}>
                  <div style={{display: 'inline', overflow: 'auto'}}>
                    <div>{item.name}</div>
                    <div className={styles.tool_description}>{item.description}</div>
                  </div>
                </div>
              ))}

            </div> : <div className={styles.empty_templates}>

            </div>
            }
          </div>
        </div> : <AgentCreate sendKnowledgeData={sendKnowledgeData} knowledge={knowledge} internalId={internalId}
                              organisationId={organisationId} sendAgentData={sendAgentData}
                              selectedProjectId={selectedProjectId} fetchAgents={fetchAgents} toolkits={toolkits}
                              template={sendTemplate} env={env}/>}
    </div>
  )
};
